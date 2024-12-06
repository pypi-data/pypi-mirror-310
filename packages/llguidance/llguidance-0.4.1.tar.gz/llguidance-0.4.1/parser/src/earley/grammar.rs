use std::{collections::HashMap, fmt::Debug, hash::Hash};

use anyhow::{bail, ensure, Result};

use crate::api::{GenGrammarOptions, GrammarId};

use super::lexerspec::{LexemeClass, LexemeIdx, LexerSpec};
use rustc_hash::FxHashMap;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct SymIdx(u32);

impl SymIdx {
    pub fn as_usize(&self) -> usize {
        self.0 as usize
    }
}

impl Symbol {
    fn is_terminal(&self) -> bool {
        self.is_lexeme_terminal()
    }
    fn is_lexeme_terminal(&self) -> bool {
        self.lexeme.is_some()
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct SymbolProps {
    pub max_tokens: usize,
    pub commit_point: bool,
    pub capture_name: Option<String>,
    pub stop_capture_name: Option<String>,
    pub hidden: bool,
    pub temperature: f32,
}

impl Default for SymbolProps {
    fn default() -> Self {
        SymbolProps {
            commit_point: false,
            hidden: false,
            max_tokens: usize::MAX,
            capture_name: None,
            stop_capture_name: None,
            temperature: 0.0,
        }
    }
}

impl SymbolProps {
    /// Special nodes can't be removed in grammar optimizations
    pub fn is_special(&self) -> bool {
        self.commit_point
            || self.hidden
            || self.max_tokens < usize::MAX
            || self.capture_name.is_some()
            || self.stop_capture_name.is_some()
    }

    pub fn for_wrapper(&self) -> Self {
        SymbolProps {
            commit_point: false,
            hidden: self.hidden,
            max_tokens: self.max_tokens,
            capture_name: None,
            stop_capture_name: None,
            temperature: self.temperature,
        }
    }

    pub fn to_string(&self) -> String {
        let props = self;
        let mut outp = String::new();

        if props.commit_point {
            if props.hidden {
                outp.push_str(" HIDDEN-COMMIT");
            } else {
                outp.push_str(" COMMIT");
            }
        }
        if props.capture_name.is_some() {
            outp.push_str(" CAPTURE");
        }

        if props.stop_capture_name.is_some() {
            outp.push_str(
                format!(
                    " STOP-CAPTURE={}",
                    props.stop_capture_name.as_ref().unwrap()
                )
                .as_str(),
            );
        }

        if props.max_tokens < 10000 {
            outp.push_str(format!(" max_tokens={}", props.max_tokens).as_str());
        }

        outp
    }
}

struct Symbol {
    idx: SymIdx,
    name: String,
    lexeme: Option<LexemeIdx>,
    gen_grammar: Option<GenGrammarOptions>,
    rules: Vec<Rule>,
    props: SymbolProps,
}

struct Rule {
    lhs: SymIdx,
    rhs: Vec<SymIdx>,
}

impl Rule {
    fn lhs(&self) -> SymIdx {
        self.lhs
    }
}

pub struct Grammar {
    name: Option<String>,
    symbols: Vec<Symbol>,
    symbol_by_name: FxHashMap<String, SymIdx>,
}

impl Grammar {
    pub fn new(name: Option<String>) -> Self {
        Grammar {
            name,
            symbols: vec![],
            symbol_by_name: FxHashMap::default(),
        }
    }

    pub fn start(&self) -> SymIdx {
        self.symbols[0].idx
    }

    pub fn is_small(&self) -> bool {
        self.symbols.len() < 200
    }

    fn sym_data(&self, sym: SymIdx) -> &Symbol {
        &self.symbols[sym.0 as usize]
    }

    fn sym_data_mut(&mut self, sym: SymIdx) -> &mut Symbol {
        &mut self.symbols[sym.0 as usize]
    }

    pub fn add_rule(&mut self, lhs: SymIdx, rhs: Vec<SymIdx>) -> Result<()> {
        let sym = self.sym_data_mut(lhs);
        ensure!(!sym.is_terminal(), "terminal symbol {}", sym.name);
        sym.rules.push(Rule { lhs, rhs });
        Ok(())
    }

    fn check_empty_symbol(&self, sym: SymIdx) -> Result<()> {
        let sym = self.sym_data(sym);
        ensure!(sym.rules.is_empty(), "symbol {} has rules", sym.name);
        ensure!(
            sym.gen_grammar.is_none(),
            "symbol {} has grammar options",
            sym.name
        );
        ensure!(sym.lexeme.is_none(), "symbol {} has lexeme", sym.name);
        Ok(())
    }

    pub fn make_terminal(
        &mut self,
        lhs: SymIdx,
        lex: LexemeIdx,
        lexer_spec: &LexerSpec,
    ) -> Result<()> {
        self.check_empty_symbol(lhs)?;
        if lexer_spec.is_nullable(lex) {
            let wrap = self.fresh_symbol_ext(
                format!("rx_null_{}", self.sym_name(lhs)).as_str(),
                self.sym_data(lhs).props.for_wrapper(),
            );
            self.sym_data_mut(wrap).lexeme = Some(lex);
            self.add_rule(lhs, vec![wrap])?;
            self.add_rule(lhs, vec![])?;
        } else {
            self.sym_data_mut(lhs).lexeme = Some(lex);
        }
        Ok(())
    }

    pub fn make_gen_grammar(&mut self, lhs: SymIdx, data: GenGrammarOptions) -> Result<()> {
        self.check_empty_symbol(lhs)?;
        let sym = self.sym_data_mut(lhs);
        sym.gen_grammar = Some(data);
        Ok(())
    }

    pub fn sym_props_mut(&mut self, sym: SymIdx) -> &mut SymbolProps {
        &mut self.sym_data_mut(sym).props
    }

    pub fn sym_name(&self, sym: SymIdx) -> &str {
        &self.symbols[sym.0 as usize].name
    }

    fn rule_to_string(&self, rule: &Rule, dot: Option<usize>) -> String {
        let ldata = self.sym_data(rule.lhs());
        let dot_data = rule
            .rhs
            .get(dot.unwrap_or(0))
            .map(|s| &self.sym_data(*s).props);
        rule_to_string(
            self.sym_name(rule.lhs()),
            rule.rhs
                .iter()
                .map(|s| self.sym_data(*s).name.as_str())
                .collect(),
            dot,
            &ldata.props,
            dot_data,
        )
    }

    fn copy_from(&mut self, other: &Grammar, sym: SymIdx) -> SymIdx {
        let sym_data = other.sym_data(sym);
        if let Some(sym) = self.symbol_by_name.get(&sym_data.name) {
            return *sym;
        }
        let r = self.fresh_symbol_ext(&sym_data.name, sym_data.props.clone());
        let self_sym = self.sym_data_mut(r);
        self_sym.lexeme = sym_data.lexeme;
        self_sym.gen_grammar = sym_data.gen_grammar.clone();
        r
    }

    fn rename(&mut self) {
        let name_repl = vec![("zero_or_more", "z"), ("one_or_more", "o")];
        for sym in &mut self.symbols {
            for (from, to) in &name_repl {
                if sym.name.starts_with(from) {
                    sym.name = format!("{}_{}", to, &sym.name[from.len()..]);
                }
            }
        }
        self.symbol_by_name = self
            .symbols
            .iter()
            .map(|s| (s.name.clone(), s.idx))
            .collect();
        assert!(self.symbols.len() == self.symbol_by_name.len());
    }

    fn expand_shortcuts(&self) -> Self {
        let mut definition = vec![None; self.symbols.len()];
        for sym in &self.symbols {
            // don't inline special symbols (commit points, captures, ...) or start symbol
            if sym.idx == self.start() || sym.props.is_special() {
                continue;
            }
            if sym.rules.len() == 1 && sym.rules[0].rhs.len() == 1 {
                uf_union(&mut definition, sym.idx, sym.rules[0].rhs[0]);
            }
        }

        uf_compress_all(&mut definition);

        let mut use_count = vec![0; self.symbols.len()];
        for sym in &self.symbols {
            if definition[sym.idx.as_usize()].is_some() {
                continue;
            }
            for r in sym.rules.iter() {
                for s in &r.rhs {
                    let s = definition[s.as_usize()].unwrap_or(*s);
                    use_count[s.0 as usize] += 1;
                }
            }
        }

        let mut repl = FxHashMap::default();

        for sym in &self.symbols {
            if sym.idx == self.start() || sym.props.is_special() {
                continue;
            }
            if sym.rules.len() == 1 && use_count[sym.idx.0 as usize] == 1 {
                // eliminate sym.idx
                repl.insert(
                    sym.idx,
                    sym.rules[0]
                        .rhs
                        .iter()
                        .map(|e| definition[e.as_usize()].unwrap_or(*e))
                        .collect::<Vec<_>>(),
                );
            }
        }

        for (idx, m) in definition.iter().enumerate() {
            if let Some(r) = m {
                repl.insert(SymIdx(idx as u32), vec![*r]);
            }
        }

        let mut simple_repl = FxHashMap::default();
        while !repl.is_empty() {
            let mut new_repl = FxHashMap::default();
            for (k, v) in repl.iter() {
                let v2 = v
                    .iter()
                    .flat_map(|s| {
                        simple_repl
                            .get(s)
                            .cloned()
                            .unwrap_or_else(|| repl.get(s).cloned().unwrap_or_else(|| vec![*s]))
                    })
                    .collect::<Vec<_>>();
                if *v == v2 {
                    simple_repl.insert(*k, v2);
                } else {
                    new_repl.insert(*k, v2);
                }
            }
            repl = new_repl;
        }
        repl = simple_repl;

        for (k, v) in repl.iter() {
            if let Some(p) = v.iter().find(|e| repl.contains_key(e)) {
                panic!("loop at {:?} ({:?})", k, p);
            }
        }

        let mut outp = Grammar::new(self.name.clone());

        let start_data = self.sym_data(self.start());
        if start_data.is_terminal() || start_data.rules.iter().any(|r| r.rhs.is_empty()) {
            let new_start = outp.fresh_symbol("_start_repl");
            outp.add_rule(new_start, vec![SymIdx(1)]).unwrap();
        }

        for sym in &self.symbols {
            if repl.contains_key(&sym.idx) {
                continue;
            }
            let lhs = outp.copy_from(self, sym.idx);
            for rule in &sym.rules {
                let rhs = rule
                    .rhs
                    .iter()
                    .flat_map(|s| repl.get(s).cloned().unwrap_or_else(|| vec![*s]))
                    .map(|s| outp.copy_from(self, s))
                    .collect();
                outp.add_rule(lhs, rhs).unwrap();
            }
        }
        outp
    }

    pub fn optimize(&self) -> Self {
        let mut r = self.expand_shortcuts();
        r = r.expand_shortcuts();
        r.rename();
        r
    }

    pub fn name(&self) -> Option<&str> {
        self.name.as_deref()
    }

    pub fn compile(&self, lexer_spec: LexerSpec) -> CGrammar {
        CGrammar::from_grammar(self, lexer_spec)
    }

    pub fn resolve_grammar_refs(
        &mut self,
        lexer_spec: &mut LexerSpec,
        ctx: &HashMap<GrammarId, (SymIdx, LexemeClass)>,
    ) -> Result<()> {
        let mut rules = vec![];
        let mut temperatures: HashMap<LexemeClass, f32> = HashMap::new();
        for sym in &mut self.symbols {
            if let Some(opts) = &sym.gen_grammar {
                if let Some((idx, cls)) = ctx.get(&opts.grammar).cloned() {
                    rules.push((sym.idx, idx));
                    let temp = opts.temperature.unwrap_or(0.0);
                    if let Some(&existing) = temperatures.get(&cls) {
                        if existing != temp {
                            bail!(
                                "temperature mismatch for nested grammar {:?}: {} vs {}",
                                opts.grammar,
                                existing,
                                temp
                            );
                        }
                    }
                    temperatures.insert(cls, temp);
                } else {
                    bail!("unknown grammar {}", opts.grammar);
                }
            }
        }
        for (lhs, rhs) in rules {
            self.add_rule(lhs, vec![rhs])?;
        }

        for sym in self.symbols.iter_mut() {
            if let Some(idx) = sym.lexeme {
                let spec = lexer_spec.lexeme_spec(idx);
                if let Some(&temp) = temperatures.get(&spec.class()) {
                    sym.props.temperature = temp;
                }
            }
        }

        Ok(())
    }

    pub fn apply_props(&mut self, sym: SymIdx, props: SymbolProps) {
        let sym = self.sym_data_mut(sym);
        if props.is_special() {
            assert!(!sym.is_terminal(), "special terminal");
        }
        assert!(
            !(!props.commit_point && props.hidden),
            "hidden on non-commit_point"
        );
        sym.props = props;
    }

    pub fn fresh_symbol(&mut self, name0: &str) -> SymIdx {
        self.fresh_symbol_ext(name0, SymbolProps::default())
    }

    pub fn fresh_symbol_ext(&mut self, name0: &str, symprops: SymbolProps) -> SymIdx {
        let mut name = name0.to_string();
        let mut idx = 2;
        while self.symbol_by_name.contains_key(&name) {
            name = format!("{}#{}", name0, idx);
            idx += 1;
        }

        let idx = SymIdx(self.symbols.len() as u32);
        self.symbols.push(Symbol {
            name: name.clone(),
            lexeme: None,
            idx,
            rules: vec![],
            props: symprops,
            gen_grammar: None,
        });
        self.symbol_by_name.insert(name, idx);
        idx
    }

    pub fn stats(&self) -> String {
        let mut num_term = 0;
        let mut num_rules = 0;
        let mut num_non_term = 0;
        let mut size = 0;
        for sym in &self.symbols {
            size += 1;
            if sym.is_terminal() {
                num_term += 1;
            } else {
                size += 1;
                num_non_term += 1;
                num_rules += sym.rules.len();
                for r in &sym.rules {
                    size += r.rhs.len();
                }
            }
        }
        format!(
            "{} terminals; {} non-terminals with {} rules with {} symbols",
            num_term, num_non_term, num_rules, size
        )
    }
}

impl Debug for Grammar {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        writeln!(f, "Grammar:")?;
        for sym in &self.symbols {
            match sym.gen_grammar {
                Some(ref opts) => {
                    writeln!(f, "{:15} ==> {:?}", sym.name, opts.grammar)?;
                }
                _ => {}
            }
            match sym.lexeme {
                Some(lx) => {
                    writeln!(
                        f,
                        "{:15} ==> [{}] temp={:.2}",
                        sym.name,
                        lx.as_usize(),
                        sym.props.temperature
                    )?;
                }
                _ => {}
            }
        }
        for sym in &self.symbols {
            if sym.rules.is_empty() {
                if sym.props.is_special() {
                    writeln!(
                        f,
                        "{:15} ⇦ {:?}  {}",
                        sym.name,
                        sym.lexeme,
                        sym.props.to_string()
                    )?;
                }
            } else {
                for rule in &sym.rules {
                    writeln!(f, "{}", self.rule_to_string(rule, None))?;
                }
            }
        }
        writeln!(f, "stats: {}\n", self.stats())?;
        Ok(())
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct CSymIdx(u16);

impl CSymIdx {
    pub const NULL: CSymIdx = CSymIdx(0);

    pub fn as_index(&self) -> usize {
        self.0 as usize
    }

    pub fn new_checked(idx: usize) -> Self {
        if idx >= u16::MAX as usize {
            panic!("CSymIdx out of range");
        }
        CSymIdx(idx as u16)
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct RuleIdx(u32);

impl RuleIdx {
    // pub const NULL: RuleIdx = RuleIdx(0);

    pub fn from_index(idx: u32) -> Self {
        RuleIdx(idx)
    }

    pub fn as_index(&self) -> usize {
        self.0 as usize
    }
}

#[derive(Clone)]
pub struct CSymbol {
    pub idx: CSymIdx,
    pub name: String,
    pub is_terminal: bool,
    pub is_nullable: bool,
    pub props: SymbolProps,
    pub gen_grammar: Option<GenGrammarOptions>,
    pub rules: Vec<RuleIdx>,
    pub sym_flags: SymFlags,
    pub lexeme: Option<LexemeIdx>,
}

#[derive(Clone, Copy)]
pub struct SymFlags(u8);

impl SymFlags {
    const COMMIT_POINT: u8 = 1 << 0;
    const HIDDEN: u8 = 1 << 2;
    const CAPTURE: u8 = 1 << 3;
    const GEN_GRAMMAR: u8 = 1 << 4;
    const STOP_CAPTURE: u8 = 1 << 5;
    const HAS_LEXEME: u8 = 1 << 6;

    fn from_csymbol(sym: &CSymbol) -> Self {
        let mut flags = 0;
        if sym.props.commit_point {
            flags |= Self::COMMIT_POINT;
        }
        if sym.props.hidden {
            flags |= Self::HIDDEN;
        }
        if sym.props.capture_name.is_some() {
            flags |= Self::CAPTURE;
        }
        if sym.gen_grammar.is_some() {
            flags |= Self::GEN_GRAMMAR;
        }
        if sym.props.stop_capture_name.is_some() {
            flags |= Self::STOP_CAPTURE;
        }
        if sym.lexeme.is_some() {
            flags |= Self::HAS_LEXEME;
        }
        SymFlags(flags)
    }

    #[inline(always)]
    pub fn commit_point(&self) -> bool {
        self.0 & Self::COMMIT_POINT != 0
    }

    #[inline(always)]
    #[allow(dead_code)]
    pub fn hidden(&self) -> bool {
        self.0 & Self::HIDDEN != 0
    }

    #[inline(always)]
    pub fn capture(&self) -> bool {
        self.0 & Self::CAPTURE != 0
    }

    #[inline(always)]
    pub fn stop_capture(&self) -> bool {
        self.0 & Self::STOP_CAPTURE != 0
    }

    #[inline(always)]
    pub fn gen_grammar(&self) -> bool {
        self.0 & Self::GEN_GRAMMAR != 0
    }

    #[inline(always)]
    pub fn has_lexeme(&self) -> bool {
        self.0 & Self::HAS_LEXEME != 0
    }
}

#[derive(Clone)]
pub struct CGrammar {
    start_symbol: CSymIdx,
    lexer_spec: LexerSpec,
    symbols: Vec<CSymbol>,
    rules: Vec<CSymIdx>,
    rule_idx_to_sym_idx: Vec<CSymIdx>,
    rule_idx_to_sym_flags: Vec<SymFlags>,
}

const RULE_SHIFT: usize = 2;

impl CGrammar {
    pub fn lexer_spec(&self) -> &LexerSpec {
        &self.lexer_spec
    }

    pub fn sym_idx_lhs(&self, rule: RuleIdx) -> CSymIdx {
        self.rule_idx_to_sym_idx[rule.as_index() >> RULE_SHIFT]
    }

    pub fn sym_flags_lhs(&self, rule: RuleIdx) -> SymFlags {
        self.rule_idx_to_sym_flags[rule.as_index() >> RULE_SHIFT]
    }

    pub fn rule_rhs(&self, rule: RuleIdx) -> (&[CSymIdx], usize) {
        let idx = rule.as_index();
        let mut start = idx - 1;
        while self.rules[start] != CSymIdx::NULL {
            start -= 1;
        }
        start += 1;
        let mut stop = idx;
        while self.rules[stop] != CSymIdx::NULL {
            stop += 1;
        }
        (&self.rules[start..stop], idx - start)
    }

    pub fn sym_data(&self, sym: CSymIdx) -> &CSymbol {
        &self.symbols[sym.0 as usize]
    }

    fn sym_data_mut(&mut self, sym: CSymIdx) -> &mut CSymbol {
        &mut self.symbols[sym.0 as usize]
    }

    pub fn sym_idx_dot(&self, idx: RuleIdx) -> CSymIdx {
        self.rules[idx.0 as usize]
    }

    #[inline(always)]
    pub fn sym_data_dot(&self, idx: RuleIdx) -> &CSymbol {
        self.sym_data(self.sym_idx_dot(idx))
    }

    pub fn start(&self) -> CSymIdx {
        self.start_symbol
    }

    pub fn rules_of(&self, sym: CSymIdx) -> &[RuleIdx] {
        &self.sym_data(sym).rules
    }

    fn add_symbol(&mut self, mut sym: CSymbol) -> CSymIdx {
        let idx = CSymIdx::new_checked(self.symbols.len());
        sym.idx = idx;
        self.symbols.push(sym);
        idx
    }

    fn from_grammar(grammar: &Grammar, lexer_spec: LexerSpec) -> Self {
        let mut outp = CGrammar {
            start_symbol: CSymIdx::NULL, // replaced
            lexer_spec,
            symbols: vec![],
            rules: vec![CSymIdx::NULL], // make sure RuleIdx::NULL is invalid
            rule_idx_to_sym_idx: vec![],
            rule_idx_to_sym_flags: vec![],
        };
        outp.add_symbol(CSymbol {
            idx: CSymIdx::NULL,
            name: "NULL".to_string(),
            is_terminal: true,
            is_nullable: false,
            rules: vec![],
            props: SymbolProps::default(),
            sym_flags: SymFlags(0),
            gen_grammar: None,
            lexeme: None,
        });

        let mut sym_map = FxHashMap::default();

        assert!(grammar.symbols.len() < u16::MAX as usize - 10);

        // lexemes go first
        for sym in grammar.symbols.iter() {
            if let Some(lx) = sym.lexeme {
                let new_idx = outp.add_symbol(CSymbol {
                    idx: CSymIdx::NULL,
                    name: sym.name.clone(),
                    is_terminal: true,
                    is_nullable: false,
                    rules: vec![],
                    props: sym.props.clone(),
                    sym_flags: SymFlags(0),
                    gen_grammar: None,
                    lexeme: Some(lx),
                });
                sym_map.insert(sym.idx, new_idx);
            }
        }

        for sym in &grammar.symbols {
            if sym.lexeme.is_some() {
                continue;
            }
            let cidx = outp.add_symbol(CSymbol {
                idx: CSymIdx::NULL,
                name: sym.name.clone(),
                is_terminal: false,
                is_nullable: sym.rules.iter().any(|r| r.rhs.is_empty()),
                rules: vec![],
                props: sym.props.clone(),
                sym_flags: SymFlags(0),
                gen_grammar: sym.gen_grammar.clone(),
                lexeme: None,
            });
            sym_map.insert(sym.idx, cidx);
        }

        outp.start_symbol = sym_map[&grammar.start()];
        for sym in &grammar.symbols {
            if sym.is_terminal() {
                assert!(sym.rules.is_empty());
                continue;
            }
            let idx = sym_map[&sym.idx];
            for rule in &sym.rules {
                // we handle the empty rule separately via is_nullable field
                if rule.rhs.is_empty() {
                    continue;
                }
                let curr = RuleIdx(outp.rules.len().try_into().unwrap());
                outp.sym_data_mut(idx).rules.push(curr);
                // outp.rules.push(idx);
                for r in &rule.rhs {
                    outp.rules.push(sym_map[r]);
                }
                outp.rules.push(CSymIdx::NULL);
            }
            while outp.rules.len() % (1 << RULE_SHIFT) != 0 {
                outp.rules.push(CSymIdx::NULL);
            }
            let rlen = outp.rules.len() >> RULE_SHIFT;
            while outp.rule_idx_to_sym_idx.len() < rlen {
                outp.rule_idx_to_sym_idx.push(idx);
            }
        }

        for sym in &mut outp.symbols {
            sym.sym_flags = SymFlags::from_csymbol(sym);
        }

        outp.rule_idx_to_sym_flags = outp
            .rule_idx_to_sym_idx
            .iter()
            .map(|s| outp.sym_data(*s).sym_flags)
            .collect();

        loop {
            let mut to_null = vec![];
            for sym in &outp.symbols {
                if sym.is_nullable {
                    continue;
                }
                for rule in sym.rules.iter() {
                    if outp
                        .rule_rhs(*rule)
                        .0
                        .iter()
                        .all(|elt| outp.sym_data(*elt).is_nullable)
                    {
                        to_null.push(sym.idx);
                    }
                }
            }
            if to_null.is_empty() {
                break;
            }
            for sym in to_null {
                outp.sym_data_mut(sym).is_nullable = true;
            }
        }

        outp
    }

    pub fn sym_name(&self, sym: CSymIdx) -> &str {
        &self.symbols[sym.0 as usize].name
    }

    pub fn rule_to_string(&self, rule: RuleIdx) -> String {
        let sym = self.sym_idx_lhs(rule);
        let symdata = self.sym_data(sym);
        let lhs = self.sym_name(sym);
        let (rhs, dot) = self.rule_rhs(rule);
        let dot_prop = if rhs.len() > 0 {
            Some(&self.sym_data_dot(rule).props)
        } else {
            None
        };
        rule_to_string(
            lhs,
            rhs.iter()
                .map(|s| self.sym_data(*s).name.as_str())
                .collect(),
            Some(dot),
            &symdata.props,
            dot_prop,
        )
    }
}

fn rule_to_string(
    lhs: &str,
    mut rhs: Vec<&str>,
    dot: Option<usize>,
    props: &SymbolProps,
    _dot_props: Option<&SymbolProps>,
) -> String {
    if rhs.is_empty() {
        rhs.push("ϵ");
        if dot == Some(0) {
            rhs.push("•");
        }
    } else if let Some(dot) = dot {
        rhs.insert(dot, "•");
    }
    format!("{:15} ⇦ {}  {}", lhs, rhs.join(" "), props.to_string())
}

fn uf_find(map: &mut [Option<SymIdx>], e: SymIdx) -> SymIdx {
    let mut root = e;
    let mut steps = 0;
    while let Some(q) = map[root.as_usize()] {
        root = q;
        steps += 1;
    }
    if steps > 1 {
        let mut p = e;
        assert!(p != root);
        while let Some(q) = std::mem::replace(&mut map[p.as_usize()], Some(root)) {
            if q == root {
                break;
            }
            p = q;
        }
    }
    root
}

fn uf_union(map: &mut [Option<SymIdx>], mut a: SymIdx, mut b: SymIdx) {
    a = uf_find(map, a);
    b = uf_find(map, b);
    if a != b {
        let r = std::mem::replace(&mut map[a.as_usize()], Some(b));
        assert!(r.is_none());
    }
}

fn uf_compress_all(map: &mut [Option<SymIdx>]) {
    for idx in 0..map.len() {
        if map[idx].is_some() {
            uf_find(map, SymIdx(idx as u32));
        }
    }
}
