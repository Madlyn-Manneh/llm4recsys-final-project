# Session 3 RQ2: history compression before reranking

Read `PROTOCOL.md` for the comparison and fixed development split. Open `rq2_h100_v2.ipynb` from this project directory in a fresh Hub kernel. Its first code cell gives the input paths, model revision, batch settings and physical GPU index. This run uses physical GPU 3 only. The notebook checks that the assigned device is idle before inference and verifies that CUDA exposes just that device.

The private `inputs.zip` bundles the frozen starter snapshot, pinned course source and FAR-Trans input archive. SHA-256 verification occurs before use. The notebook can reuse the verified checkpoint under the configured scratch root's `models/Qwen3-1.7B-70d244cc/`, or assemble it from the staged pieces there. The first launch stopped during model assembly because the Hub home volume filled up. The revised launch changes only its model and results paths. Neither public weights nor customer data belong in Git.

The run writes inference logs and rankings to `results/rq2_h100_v2/` and leaves `progress.json` for a live status check. `evaluate_rq2_v2.ipynb` reads those files without loading an LLM. Reproduce with the same ordered contexts to avoid changes from CBF near ties. The printed protocol hash alone does not guarantee identical candidate order across machines.
