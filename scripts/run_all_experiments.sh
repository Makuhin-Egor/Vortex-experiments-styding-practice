#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$BASE_DIR/results/raw_logs"


mkdir -p "$LOG_DIR"

# Путь к Vortex. Если у вас структура папок стандартная (рядом), то сработает по умолчанию.
# Если нет, то запустите скрипт так: VORTEX_BUILD=/custom/path bash scripts/run_all_experiments.sh
VORTEX_BUILD="${VORTEX_BUILD:-$BASE_DIR/../vortex/build}"

cd "$VORTEX_BUILD" || { echo "Error: Vortex build not found at $VORTEX_BUILD. Please set VORTEX_BUILD variable."; exit 1; }

echo "Starting Vortex Experiments..."
echo "Vortex build dir: $(pwd)"
echo "Logs will be saved to: $LOG_DIR"
sleep 2

# Функция для запуска теста
run_test() {
    local test_name=$1
    local cores=$2
    local cache_flags=$3
    local app=$4
    local args=$5

    echo "Running: $test_name..."
        ./ci/blackbox.sh --cores="$cores" "$cache_flags" --app="$app" --args="$args" > "$LOG_DIR/${test_name}.log" 2>&1
}

# -------------------------------------
# ЭКСПЕРИМЕНТЫ
# -------------------------------------
run_test "vecadd_strong_1c_noL2" 1 "" "vecadd" "-n16384"
run_test "vecadd_strong_2c_noL2" 2 "" "vecadd" "-n16384"
run_test "vecadd_strong_4c_noL2" 4 "" "vecadd" "-n16384"

run_test "vecadd_strong_1c_L2" 1 "--l2cache" "vecadd" "-n16384"
run_test "vecadd_strong_2c_L2" 2 "--l2cache" "vecadd" "-n16384"
run_test "vecadd_strong_4c_L2" 4 "--l2cache" "vecadd" "-n16384"
run_test "vecadd_strong_4c_L2L3" 4 "--l2cache --l3cache" "vecadd" "-n16384"

run_test "vecadd_weak_2c_noL2" 2 "" "vecadd" "-n32768"
run_test "vecadd_weak_4c_noL2" 4 "" "vecadd" "-n65536"

echo "All automated experiments finished! Check results/raw_logs/"
