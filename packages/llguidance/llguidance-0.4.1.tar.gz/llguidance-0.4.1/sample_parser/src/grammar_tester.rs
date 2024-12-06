use llguidance_parser::{
    api::{GrammarWithLexer, ParserLimits, TopLevelGrammar},
    toktrie::{InferenceCapabilities, TokEnv, TokenId},
    Constraint, TokenParser,
};

use lazy_static::lazy_static;

/// Check that the grammar generates the expected output.
///
/// Output is a list of strings, each of which is a sequence of tokens.
/// Tokens in the string are separated with "‧".
/// Strings at even positions are "forced tokens", and strings at odd positions
/// are "generated tokens".
/// We check that the grammars forces the forced tokens (first of which is the
/// prompt), and that it allows in the mask the generated tokens.
///
/// These tests are "recorded" by passing "test_trace": true in the llguidance
/// request and post-processing.
fn check_grammar(
    tok_env: &TokEnv,
    prompt_str: &str,
    grammar: TopLevelGrammar,
    output: &[&str],
    temp: f32,
) {
    println!("\nChecking grammar");

    let parser = TokenParser::from_llguidance_json(
        tok_env.clone(),
        grammar,
        llguidance_parser::Logger::new(0, 2),
        InferenceCapabilities {
            ff_tokens: true, // can the engine append multiple tokens?
            backtrack: true, // can the engine remove generated tokens?

            conditional_ff_tokens: false, // not used
            fork: false,                  // not used
        },
        ParserLimits::default(),
        vec![],
    )
    .unwrap();
    let mut constraint = Constraint::new(parser);

    let prompt = constraint.process_prompt(tok_env.tokenize(prompt_str));
    check_eq(tok_env, "prompt", &prompt, output[0]);

    let mut idx = 1;
    let mut gen_tokens = tokenize_trace(tok_env, output[idx]);
    let mut seen_temp = temp == 0.0;

    for _ in 0..200 {
        let res = constraint.compute_mask().unwrap();

        if let Some(t) = res.temperature {
            assert!(
                t == temp || t == 0.0,
                "Expected temperature {} got {}",
                temp,
                t
            );
            if t == temp {
                seen_temp = true;
            }
        }

        if res.is_stop() {
            assert!(idx >= output.len() - 1, "Expected more output at {}", idx);
            assert!(gen_tokens.is_empty(), "Expected more tokens to generate");
            break;
        }

        let mut bt: u32;
        let mut toks: Vec<TokenId>;

        if let Some(mask) = &res.sample_mask {
            if gen_tokens.is_empty() {
                panic!("No more tokens to generate");
            }
            let tok = gen_tokens.remove(0);
            assert!(mask.is_allowed(tok), "Token {} not allowed", tok);
            let res = constraint.commit_token(Some(tok)).unwrap();
            bt = res.backtrack;
            toks = res.ff_tokens.clone();
            if toks.is_empty() || toks[0] != tok {
                if output[idx + 1].starts_with("1↶") {
                    // fast-forward with fake backtrack
                    assert!(bt == 0 || res.ff_tokens.is_empty());
                    bt = 1;
                    // go to forced byte checking
                } else {
                    panic!("Expected token {} got {}", tok, toks[0]);
                }
            } else if toks.len() > 1 {
                // we got fast-forwarded to the next entry,
                // delete the generated tokens and leave the rest for forced
                // bytes checking below
                toks.remove(0);
                // go to forced byte checking
            } else {
                assert!(bt == 0);
                assert!(toks.len() == 1);
                continue; // normal path
            }
        } else {
            let res = constraint.commit_token(None).unwrap();
            bt = res.backtrack;
            toks = res.ff_tokens.clone();
        }

        // forced byte checking
        assert!(gen_tokens.is_empty(), "Expected more tokens to generate");

        idx += 1;
        let mut expected = output[idx];
        if expected.contains("↶") {
            let parts: Vec<&str> = expected.split("↶").collect();
            assert!(parts.len() == 2);
            expected = parts[1];
            assert!(
                bt == parts[0].parse::<u32>().unwrap(),
                "Expected backtrack {} got {}",
                parts[0],
                bt
            );
        }
        check_eq(tok_env, &format!("step {}", idx), &toks, expected);
        idx += 1;
        if idx < output.len() {
            gen_tokens = tokenize_trace(tok_env, output[idx]);
        }
    }

    assert!(seen_temp, "Expected temperature {} not seen", temp);
}

fn check_eq(tok_env: &TokEnv, label: &str, tokens: &[TokenId], expected_tokens: &str) {
    let trie = tok_env.tok_trie();
    let actual_tokens = trie.test_trace_tokens(tokens);
    println!(
        "Checking {}: exp:{:?} got:{:?}",
        label, expected_tokens, actual_tokens
    );
    assert_eq!(
        actual_tokens, expected_tokens,
        "Tokens mismatch in {}",
        label
    );
}

fn tokenize_trace(tok_env: &TokEnv, s: &str) -> Vec<TokenId> {
    let trie = tok_env.tok_trie();
    println!("Tokenizing {:?}", s);
    let mut result = Vec::new();
    for word in s.split("‧") {
        if word == "≺EOS≻" {
            result.push(trie.eos_token());
            continue;
        }
        let tt = trie.greedy_tokenize(word.as_bytes());
        assert!(
            tt.len() == 1,
            "Expected single token for {:?} got {:?}",
            word,
            tt
        );
        result.push(tt[0]);
    }
    result
}

lazy_static! {
    static ref TOK_ENV: TokEnv = {
        toktrie_hf_tokenizers::ByteTokenizerEnv::from_name("microsoft/Phi-3.5-mini-instruct", None)
            .unwrap()
            .to_env()
    };
}

fn check_lark_grammar_prompt(lark: &str, prompt_str: &str, output: &[&str]) {
    let grm = TopLevelGrammar::from_lark(lark.to_string());
    check_grammar(&TOK_ENV, prompt_str, grm, output, 0.0);
}

fn check_lark_grammar(lark: &str, output: &[&str]) {
    check_lark_grammar_prompt(lark, "", output);
}

fn check_lark_grammar_nested(lark: &str, sub_lark: &str, output: &[&str]) {
    let temp = lark
        .find("temperature=")
        .map(|i| {
            let i = i + "temperature=".len();
            let mut end = i;
            while end < lark.len()
                && (lark.as_bytes()[end].is_ascii_digit() || lark.as_bytes()[end] == b'.')
            {
                end += 1;
            }
            lark[i..end].parse::<f32>().unwrap()
        })
        .unwrap_or(0.0);
    let mut top_grm = TopLevelGrammar::from_lark(lark.to_string());
    let mut sub_grm = GrammarWithLexer::from_lark(sub_lark.to_string());
    sub_grm.name = Some("sub".to_string());
    top_grm.grammars.push(sub_grm);
    check_grammar(&TOK_ENV, "", top_grm, output, temp);
}

fn test_ll_skip() {
    check_lark_grammar(
        r#"start: "A" "!"
           %ignore /[ \t]+/"#,
        &["A", " ‧ ‧!"],
    );

    check_lark_grammar(
        r#"
            start: "A: " NUMBER
            NUMBER: /[0-9]+/
            %ignore /[ \t]+/
        "#,
        &["A‧:", " ‧ ‧5‧6‧≺EOS≻"],
    );

    check_lark_grammar_nested(
        r#"start: "." @sub"#,
        r#"start: "A" "!"
           %ignore /[ \t]+/"#,
        &[".‧A", " ‧ ‧!"],
    );
}

fn test_ll_temperature() {
    check_lark_grammar_nested(
        r#"start: /[xy]/ sub_temp
           sub_temp[temperature=0.5]: @sub
        "#,
        r#"start: "[" ("A")* "]"
           %ignore /[ \t]+/"#,
        &["", "x‧[‧]"],
    );

    check_lark_grammar_nested(
        r#"start: sub_temp
           sub_temp[temperature=0.5]: @sub
        "#,
        r#"start: "[" ("A")* "]"
           %ignore /[ \t]+/"#,
        &["", "[‧]"],
    );

    check_lark_grammar_nested(
        r#"start: sub_temp
           sub_temp[temperature=0.5]: @sub
        "#,
        r#"start: "[" ("A")* "]"
           %ignore /[ \t]+/"#,
        &["", "[]"],
    );

    check_lark_grammar_nested(
        r#"start: sub_temp
           sub_temp[temperature=0.5]: @sub
        "#,
        r#"start: "[" ("A")* "]"
        "#,
        &["", "[‧]"],
    );
}

fn test_ll_backtrack_stop() {
    check_lark_grammar(
        r#"
            start: "Count to 10: 1, 2, 3, 4, 5, 6, 7, " text "\nNot quite."
            text[stop=","]: /.+/
        "#,
        &[
            "Count‧ to‧ ‧1‧0‧:‧ ‧1‧,‧ ‧2‧,‧ ‧3‧,‧ ‧4‧,‧ ‧5‧,‧ ‧6‧,‧ ‧7‧,",
            " ‧8‧,",
            "1↶\n‧Not‧ quite‧.",
        ],
    );

    check_lark_grammar(
        r#"
            start: "Name: " name "\nName: " name
            name[stop=STOP]: /E[a-z]+/
            STOP: /[a-b]/ | /[x-z]/
        "#,
        &["Name‧:", " Em‧ily", "1↶il‧\n‧Name‧:", " Emil‧ie‧a", "1↶"],
    );
}

fn test_llparser() {
    check_lark_grammar_prompt(
        r#"
            start: gen
            gen[stop=""]: /.*/
        "#,
        "2 + 2 =",
        &["2‧ +‧ ‧2", " =>‧ ‧4‧≺EOS≻"],
    );

    check_lark_grammar(
        r#"
            start: "Power frequency is " num "Hz; voltage is " num "V"
            num[stop="", max_tokens=5]: /[0-9]+/
        "#,
        &[
            "Power‧ frequency‧ is‧ ",
            "5‧0‧Hz", // no EoS needed on 50Hz
            ";‧ voltage‧ is‧ ",
            "2‧2‧0‧V",
        ],
    );

    check_lark_grammar(
        r#"
            start: "Power frequency is " num "Hz; voltage is " num "V"
            num[stop="", max_tokens=3]: /[0-9]+/
        "#,
        &[
            "Power‧ frequency‧ is‧ ",
            "5‧0‧Hz", // no EoS needed on 50Hz
            ";‧ voltage‧ is‧ ",
            "2‧2‧0",
            "V", // V is forced since max_tokens=3
        ],
    );

    check_lark_grammar(
        r#"
            start: "Q: Are dolphins fish?\nA: " ANSWER "\nQ: Are sharks fish?\nA: " ANSWER
            ANSWER: "Yes" | "No"
        "#,
        &[
            "Q‧:‧ Are‧ dol‧ph‧ins‧ fish‧?‧\n‧A‧:",
            " No", // note the prefix space - moved by token healing
            "\n‧Q‧:‧ Are‧ sh‧arks‧ fish‧?‧\n‧A‧:",
            " Yes",
        ],
    );

    check_lark_grammar(
        r#"
            start: "Q: 7 * 8\nA: " NUMBER
            NUMBER: /[0-9]+/
        "#,
        &["Q‧:‧ ‧7‧ *‧ ‧8‧\n‧A‧:‧ ", "5‧6‧≺EOS≻"],
    );
}

fn test_ll_nullable_lexeme() {
    // Emake sure 'a' is not forced
    check_lark_grammar(
        r#"start: gen
           gen[stop=""]: /a*/"#,
        &["", "a‧≺EOS≻"],
    );

    // this one doesn't work - no lexeme was scanned by EOS, so we allow more lexemes...
    check_lark_grammar(
        r#"start: gen
           gen[stop=""]: /a*/"#,
        &["", "≺EOS≻"],
    );

    // see that we can skip 5*
    check_lark_grammar(
        r#"start: "6 * 7 = " five_seq num "\n"
           five_seq[stop=""]: /5*/
           num[stop=""]: /[1-4][0-9]/"#,
        &["6‧ *‧ ‧7‧ =‧ ", "4‧2", "\n"],
    );

    check_lark_grammar_nested(
        r#"start: "Here: 2 + 2 = " @sub"#,
        r#"start: /[0-9]+/"#,
        &["Here‧:‧ ‧2‧ +‧ ‧2‧ =‧ ", "4‧≺EOS≻"],
    );

    // make sure it stops at EOS
    check_lark_grammar_nested(
        r#"start: "Here: 2 + 2 = " @sub"#,
        r#"start: num q
           num: /[0-9]+/
           q: /Q?/
        "#,
        &["Here‧:‧ ‧2‧ +‧ ‧2‧ =‧ ", "4‧≺EOS≻"],
    );

    let float_grammar = r#"
        start: num1 | num2
        num1: /-?(?:0|[1-9][0-9]*)/
        num2: /-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)/
    "#;
    check_lark_grammar_nested(r#"start: @sub"#, &float_grammar, &["", "1‧≺EOS≻"]);
    check_lark_grammar_nested(r#"start: @sub"#, &float_grammar, &["", "0‧≺EOS≻"]);
    check_lark_grammar_nested(r#"start: @sub"#, &float_grammar, &["", "1‧.‧1‧≺EOS≻"]);
    check_lark_grammar_nested(r#"start: @sub"#, &float_grammar, &["", "0‧.‧1‧≺EOS≻"]);
}

fn main() {
    test_llparser();
    test_ll_backtrack_stop();
    test_ll_nullable_lexeme();
    test_ll_skip();
    test_ll_temperature();
}
