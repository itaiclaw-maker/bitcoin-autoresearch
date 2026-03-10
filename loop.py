import os
import json
import shutil
import subprocess
import time
import asyncio
from pathlib import Path
from backtest import evaluate

# OpenClaw-specific imports will be used via sessions_spawn
# This script orchestrates the evolutionary loop

BASE_DIR = Path(__file__).parent
BEST_STRATEGY = BASE_DIR / "strategy_best.py"
CANDIDATE_STRATEGY = BASE_DIR / "strategy_candidate.py"
PROGRAM_MD = BASE_DIR / "program.md"
RESULTS_LOG = BASE_DIR / "results_log.jsonl"

def log_iteration(iteration, result, improved):
    entry = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "iteration": iteration,
        "score": result['score'],
        "sharpe": result.get('sharpe'),
        "max_drawdown": result.get('max_drawdown'),
        "n_trades": result.get('n_trades'),
        "improved": improved
    }
    with open(RESULTS_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")

async def run_iterations(count=10):
    if not BEST_STRATEGY.exists():
        shutil.copy(BASE_DIR / "strategy.py", BEST_STRATEGY)
    
    best_res = evaluate(str(BEST_STRATEGY))
    best_score = best_res['score']
    
    # Get start iteration from log
    start_iter = 1
    if RESULTS_LOG.exists():
        with open(RESULTS_LOG, "r") as f:
            lines = f.readlines()
            if lines:
                last_entry = json.loads(lines[-1])
                start_iter = last_entry.get("iteration", 0) + 1

    print(f"🛰️ Resuming from Iteration {start_iter}. Current Best Sharpe: {best_score:.4f}")

    for i in range(start_iter, start_iter + count):
        print(f"\n🚀 [Iteration {i}] Evolving strategy...")
        
        # In a full autonomous run, we'd use sessions_spawn here.
        # Since I am the main agent, I will perform the 'mutation' logic 
        # by analyzing the results and rewriting strategy_candidate.py.
        # This keeps the loop tight within this session for the 10-run burst.
        
        # This is a placeholder for the "Main Agent Mutation" logic
        # which will be handled in the next turns.
        break 

if __name__ == "__main__":
    asyncio.run(run_iterations(10))
