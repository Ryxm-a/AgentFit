from agentfit.extract import extract_capabilities

def test_ghidra_wasm_task_matches_expected_tags():
    tags={c.tag for c in extract_capabilities("I want to reverse engineer a WebAssembly binary in Ghidra")}
    assert "ghidra" in tags and "reverse-engineering" in tags and "webassembly" in tags
def test_wordpress_audit_task_matches_security():
    tags={c.tag for c in extract_capabilities("Audit this WordPress plugin for vulnerabilities")}
    assert {"wordpress","security","vulnerability-scanning"}<=tags
def test_unmatched_task_falls_back_to_generic_keywords():
    caps=extract_capabilities("juggle flaming kittens professionally");assert len(caps)==1 and caps[0].tag.startswith("general:") and caps[0].confidence<.5
def test_empty_task_yields_no_capabilities():assert extract_capabilities("")==[]
