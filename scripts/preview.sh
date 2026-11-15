#!/usr/bin/env bash
#
# Sobe o site da Enciclopedia Visual localmente.
#
#   ./scripts/preview.sh            # build completo + servidor em :4173
#   ./scripts/preview.sh --no-build # so re-sincroniza e reconstroi
#   PORT=8080 ./scripts/preview.sh   # porta alternativa
#
# Requisitos: Node 22+ e Python 3.9+.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SITE_DIR="${QUARTZ_DIR:-$ROOT/site}"
QUARTZ_REPO="${QUARTZ_REPO:-https://github.com/jackyzha0/quartz.git}"
QUARTZ_REF="${QUARTZ_REF:-v5}"
PORT="${PORT:-4173}"

cd "$ROOT"

if [ ! -d "$SITE_DIR/.git" ]; then
  echo "==> Clonando Quartz ($QUARTZ_REF) em $SITE_DIR"
  git clone --depth 1 --branch "$QUARTZ_REF" "$QUARTZ_REPO" "$SITE_DIR"
fi

if [ ! -d "$SITE_DIR/node_modules" ]; then
  echo "==> Instalando dependencias"
  (cd "$SITE_DIR" && npm ci --no-audit --no-fund)
fi

echo "==> Sincronizando conteudo do cofre"
python3 scripts/sync_content.py --dest "$SITE_DIR/content"
cp "$ROOT/quartz.config.yaml" "$SITE_DIR/quartz.config.yaml"

echo "==> Instalando plugins"
(cd "$SITE_DIR" && npx quartz plugin install)

if [ "${1:-}" != "--no-build" ]; then
  echo "==> Build"
  (cd "$SITE_DIR" && npx quartz build)
fi

echo ""
echo "==> Servindo em http://localhost:$PORT"
echo "    (Ctrl+C para parar)"
echo ""
cd "$SITE_DIR"
exec npx quartz build --serve --port "$PORT"
