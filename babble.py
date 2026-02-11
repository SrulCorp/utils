import random, time, sys, shutil, math
from datetime import datetime

TERM_WIDTH = shutil.get_terminal_size((100, 20)).columns

DESYNC = False
DESYNC_DECAY = 0.0

# =========================
# Terminal Coloring (ANSI)
# =========================

class C:
    RESET  = "\033[0m"
    DIM    = "\033[2m"
    BOLD   = "\033[1m"

    RED    = "\033[31m"
    GREEN  = "\033[32m"
    YELLOW = "\033[33m"
    BLUE   = "\033[34m"
    MAG    = "\033[35m"
    CYAN   = "\033[36m"
    GRAY   = "\033[90m"

if not sys.stdout.isatty():
    for a in vars(C):
        if a.isupper():
            setattr(C, a, "")

LEVEL_COLORS = {
    "DEBUG": C.CYAN,
    "INFO":  C.GREEN,
    "WARN":  C.YELLOW,
    "ERROR": C.RED,
}

# =========================
# Expanded Vocabulary
# =========================

verbs = [
    "Optimizing","Calibrating","Initializing","Compiling","Resolving","Stabilizing",
    "Rebuilding","Validating","Encrypting","Normalizing","Indexing","Vectorizing",
    "Rebalancing","Parallelizing","Flushing","Reprocessing",
    "Bootstrapping","Checkpointing","Rehydrating","Reconciling",
    "Synchronizing","Snapshotting","Migrating","Refactoring","Defragmenting",
    "Orchestrating","Prefetching","Streaming","Decoding","Encoding",
    "Provisioning","Instrumenting","Hardening","Sanitizing","Remapping",
    "Throttling","Uplinking","Downlinking","Decompressing","Compressing"
]

adjectives = [
    "distributed","cached","asynchronous","threaded","buffered","segmented",
    "redundant","streamed","batched","persistent","virtualized","isolated",
    "replicated","compressed","sharded","event-driven","fault-tolerant",
    "elastic","containerized","stateless","stateful","latency-sensitive",
    "throughput-bound","compute-heavy","memory-bound","I/O-bound","ephemeral",
    "transactional","deterministic","adaptive","self-healing"
]

nouns = [
    "memory regions","task queues","execution pipelines","data caches",
    "runtime contexts","I/O buffers","compute graphs","event streams",
    "process tables","thread pools","log buffers","scheduler state",
    "control plane","data plane","routing fabric","metadata store",
    "commit log","job dispatcher","resource manager","service mesh",
    "state vectors","priority heaps","checkpoint archives",
    "replica sets","consensus ledger","signal bus","event broker"
]

metrics = [
    "latency_ms","throughput_ops","mem_used_mb","cpu_util_pct","disk_io_mb",
    "cache_hit_ratio","queue_depth","packet_loss_pct","response_ms",
    "thread_util_pct","gc_pause_ms","swap_mb","ctx_switch_rate",
    "lock_wait_ms","heap_frag_pct","scheduler_jitter_ms",
    "bandwidth_util_pct","page_fault_rate","retry_rate",
    "stall_cycles","commit_latency_ms","replica_lag_ms","event_backpressure"
]

errors_1 = [
    "Clock skew detected",
    "Transient memory pressure",
    "Scheduler starvation warning",
    "Buffer boundary violation",
    "Deadlock hazard identified",
    "Latency excursion outside SLA",
    "Process sync failure",
    "Heap fragmentation exceeded limit",
    "Priority inversion condition",
    "Replica divergence threshold exceeded",
    "Consensus quorum timeout",
    "Checkpoint integrity failure",
    "Transaction rollback surge",
    "Kernel watchdog expiry",
    "Event loop saturation"
]

fixes_1 = [
    "reallocating memory pools",
    "resetting scheduler weights",
    "flushing I/O pipelines",
    "restarting stalled workers",
    "rebuilding cache indices",
    "resynchronizing system clocks",
    "compacting heap segments",
    "forcing scheduler rebalance",
    "replaying transaction journal",
    "invalidating replica caches",
    "reconstructing checkpoint archive",
    "initiating leader re-election",
    "reinitializing event loop",
    "throttling inbound traffic"
]

distributed_tasks = [
    "Synchronizing worker pools","Rebalancing task partitions",
    "Propagating state deltas","Merging result buffers",
    "Reconciling cache entries","Replicating shard segments",
    "Broadcasting control frames","Realigning node clocks",
    "Consolidating memory pages","Reassigning execution slots",
    "Checkpointing compute state","Streaming telemetry snapshots",
    "Validating quorum integrity"
]

LOG_LEVELS = ["DEBUG","INFO","WARN","ERROR"]
NODES = [f"node-{i:02d}" for i in range(1,9)]

PIPELINE_STAGES = [
    "Input Parsing","Schema Validation","Task Scheduling","Resource Allocation",
    "Parallel Execution","Result Aggregation","Output Serialization","Final Commit"
]

ERRORS_2 = [
    "Clock skew","Thread deadlock","Memory exhaustion",
    "Queue saturation","Race condition",
    "Scheduler stall","Quorum degradation","Heap corruption"
]

FIXES_2 = [
    "restarting scheduler",
    "draining execution queues",
    "reallocating memory pools",
    "resetting worker threads",
    "resynchronizing system clock",
    "forcing leader re-election",
    "replaying commit log",
    "invalidating stale replicas"
]

# =========================
# Helpers
# =========================

def ts():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]

def log(level, msg, node=None):
    color = LEVEL_COLORS.get(level, "")
    p = f"{C.GRAY}[{ts()}]{C.RESET} {color}[{level:<5}]{C.RESET}"
    if node:
        p += f" {C.MAG}[{node}]{C.RESET}"
    print(f"{p} {msg}")

def rand_delay(base=0.02, spread=0.4):
    return max(0.003, random.lognormvariate(math.log(base), spread))

LAST_PROGRESS = 0
PROGRESS_COOLDOWN = (6.0, 16.0)

def can_show_progress():
    global LAST_PROGRESS
    now = time.time()
    if now - LAST_PROGRESS > random.uniform(*PROGRESS_COOLDOWN):
        LAST_PROGRESS = now
        return True
    return False

def animated_progress(label, width=40, fail_chance=0.006):
    bar_width = min(width, TERM_WIDTH - len(label) - 20)
    p = 0

    speed_profile = random.choice([
        (1, 4, 0.015, 0.05),
        (2, 6, 0.01, 0.04),
        (3, 8, 0.02, 0.08),
    ])

    step_min, step_max, t_min, t_max = speed_profile

    while p <= 100:
        filled = int(bar_width * p / 100)
        bar = (
            f"{C.BLUE}[{C.GREEN}{'█'*filled}{C.GRAY}{'-'*(bar_width-filled)}"
            f"{C.BLUE}]{C.RESET} {C.BOLD}{p:3d}%{C.RESET}"
        )
        print(f"\r{C.CYAN}{label:<48}{C.RESET} {bar}", end="", flush=True)
        time.sleep(random.uniform(t_min, t_max))
        p += random.randint(step_min, step_max)

    print()

# =========================
# Script 1
# =========================

def random_metrics():
    return f"{C.YELLOW}{random.choice(metrics)}{C.RESET}={C.CYAN}{random.uniform(0.01,999.99):.2f}{C.RESET}"

def generate_process():
    if random.random() < 0.30:
        return f"{random.choice(verbs)} and {random.choice(verbs).lower()} {random.choice(adjectives)} {random.choice(nouns)}"
    return f"{random.choice(verbs)} {random.choice(adjectives)} {random.choice(nouns)}"

def script1_cycle():
    r = random.random()

    if r < 0.50 and can_show_progress():
        animated_progress(generate_process(), 48)
    elif r < 0.985:
        print("Updating operational metrics → " +
              ", ".join(random_metrics() for _ in range(random.randint(2,4))))
    else:
        err = random.choice(errors_1)
        fix = random.choice(fixes_1)

        log("WARN", err)
        time.sleep(random.uniform(0.4,1.0))
        log("INFO", f"Executing remediation: {fix}")
        time.sleep(random.uniform(0.5,1.2))
        log("INFO", "Subsystem stabilized")

# =========================
# Script 2
# =========================

def ascii_graph(lbl, val, m=100):
    w = 30
    b = int(w*val/m)
    return (
        f"{C.BOLD}{lbl:<6}{C.RESET} |"
        f"{C.GREEN}{'█'*b}{C.GRAY}{' '*(w-b)}{C.RESET}| "
        f"{C.CYAN}{val:6.2f}%{C.RESET}"
    )

def telemetry():
    for k,a,b in [("CPU",8,85),("GPU",3,88),("MEM",20,80),("NET",5,75)]:
        print(ascii_graph(k, random.uniform(a,b)))

def pipeline_stage(stage):
    animated_progress(stage, 50, fail_chance=0.008)

def pipeline_sim():
    log("INFO","Launching multi-stage execution pipeline")
    for stage in PIPELINE_STAGES:
        pipeline_stage(stage)
    log("INFO","Pipeline execution completed successfully")

def glitch_2(node):
    log("WARN", f"{random.choice(ERRORS_2)} detected", node)
    time.sleep(random.uniform(0.6,1.4))
    log("INFO", f"Applying correction via {random.choice(FIXES_2)}", node)
    time.sleep(random.uniform(0.5,1.2))
    log("INFO","Node stabilized", node)

def distributed_activity():
    log("DEBUG", random.choice(distributed_tasks), random.choice(NODES))

def script2_cycle():
    r = random.random()

    if r < 0.20 and can_show_progress():
        pipeline_sim()
    elif r < 0.50:
        log("INFO","Telemetry snapshot")
        telemetry()
    elif r < 0.80:
        distributed_activity()
    elif r < 0.98:
        glitch_2(random.choice(NODES))
    else:
        log("ERROR","Critical service disruption")
        time.sleep(random.uniform(1.0,2.5))
        log("INFO","Core services restored")

# =========================
# Master Loop
# =========================

try:
    log("INFO","Hybrid Processing Engine online")
    while True:
        if random.random() < 0.00015:
            log("ERROR","System-wide fault cascade detected")
            time.sleep(random.uniform(1.5,3.0))
            log("INFO","Global recovery complete")
        else:
            (script1_cycle if random.random() < 0.55 else script2_cycle)()
        time.sleep(rand_delay(0.03,0.7))

except KeyboardInterrupt:
    log("ERROR","Process terminated — unrecoverable interrupt")
    raise RuntimeError("Fatal runtime interruption")
