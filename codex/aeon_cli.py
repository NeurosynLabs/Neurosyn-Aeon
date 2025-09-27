def main():
    ap = argparse.ArgumentParser(prog="aeon", description="Vault Codex × AEON bridge")
    ap.add_argument("--aeon", default="AEON.json")
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("init")
    sp.add_parser("build")
    p = sp.add_parser("seal"); p.add_argument("name")
    sp.add_parser("audit")
    args = ap.parse_args()

    full_cfg = read_json(args.aeon)

    # Accept BOTH formats:
    # 1) AEON.json with {"vault_bridge": {...}}
    # 2) Standalone VAULT_BRIDGE.json with the bridge object at root
    in_aeon_wrapper = isinstance(full_cfg, dict) and "vault_bridge" in full_cfg
    v = full_cfg["vault_bridge"] if in_aeon_wrapper else full_cfg

    cmd_map = {"init": init_cmd, "build": build_cmd, "seal": seal_cmd, "audit": audit_cmd}
    result = cmd_map[args.cmd](args, v)

    # Write back to the same file that was read
    if in_aeon_wrapper:
        full_cfg["vault_bridge"] = v
        write_json(args.aeon, full_cfg)
    else:
        write_json(args.aeon, v)

    # Print something non-fatal if the command produced paths (build)
    if isinstance(result, list):
        for p in result: print(f"artifact: {p}")
