#!/bin/bash

# スクリプトが配置されているディレクトリに移動 (任意だが安全のため)
cd "$(dirname "$0")" || exit

# --- 設定 ---
IMAGE_NAME="smly/mjai-client:v3"
CONTAINER_NAME="mjai_bot_container" # コンテナに名前をつけると管理しやすい
HOST_PORT="28080"
CONTAINER_PORT="3000"
SUBMISSION_ZIP="submission.zip"
WORKSPACE_DIR="/workspace" # コンテナ内の作業ディレクトリ
INTERACTIVE_MODE=false # デフォルトは自動入力モード

# --- 引数処理 ---
# -i または --interactive が指定されたらインタラクティブモードにする
if [[ "$1" == "-i" ]] || [[ "$1" == "--interactive" ]]; then
    INTERACTIVE_MODE=true
    echo "Running in interactive mode."
else
    echo "Running in automatic input mode."
    # ここで他の引数オプションを追加することも可能
fi

# --- 前準備 ---
echo "1. Creating submission zip file..."
python scripts/create_submission.py
if [ $? -ne 0 ]; then
    echo "Error: Failed to create $SUBMISSION_ZIP"
    exit 1
fi
echo "$SUBMISSION_ZIP created successfully."

echo "2. Stopping and removing existing container (if any)..."
docker stop $CONTAINER_NAME > /dev/null 2>&1
docker rm $CONTAINER_NAME > /dev/null 2>&1
echo "Existing container stopped and removed."

# --- コンテナ起動 ---
echo "3. Starting new container $CONTAINER_NAME..."
# submission.zip をコンテナ内の /tmp にコピーするようにマウント
# sleep infinity でコンテナを起動し続ける
CONTAINER_ID=$(docker run --platform linux/amd64 -d --rm --name $CONTAINER_NAME \
                -p $HOST_PORT:$CONTAINER_PORT \
                --mount "type=bind,src=$(pwd)/$SUBMISSION_ZIP,dst=/tmp/$SUBMISSION_ZIP,readonly" \
                $IMAGE_NAME sleep infinity)

if [ -z "$CONTAINER_ID" ]; then
    echo "Error: Failed to start container."
    exit 1
fi
echo "Container $CONTAINER_ID started."

# --- コンテナ内での準備 ---
echo "4. Unzipping submission file inside the container..."
# コンテナ内にワークスペースディレクトリを作成
docker exec $CONTAINER_ID mkdir -p $WORKSPACE_DIR
# /tmp/submission.zip を /workspace に展開
docker exec $CONTAINER_ID unzip -q /tmp/$SUBMISSION_ZIP -d $WORKSPACE_DIR
if [ $? -ne 0 ]; then
    echo "Error: Failed to unzip $SUBMISSION_ZIP in the container."
    docker stop $CONTAINER_ID # エラー時はコンテナを停止
    exit 1
fi
echo "Unzipped successfully to $WORKSPACE_DIR."

# --- ボット実行 ---
if [ "$INTERACTIVE_MODE" = true ]; then
    # インタラクティブモード
    echo "5. Running the bot script interactively..."
    # -it オプションで対話的に実行
    docker exec -it -w $WORKSPACE_DIR $CONTAINER_ID \
           $WORKSPACE_DIR/.pyenv/shims/python -u bot.py 0
    # ユーザーが手動でJSONを入力する
else
    # 自動入力モード
    echo "5. Running the bot script with predefined input..."
    # -i オプションとヒアドキュメントで自動入力
    cat << 'EOF' | docker exec -i -w $WORKSPACE_DIR $CONTAINER_ID \
           $WORKSPACE_DIR/.pyenv/shims/python -u bot.py 0
[{"type":"start_game","id":0}]
[{"type":"start_kyoku","bakaze":"E","dora_marker":"2s","kyoku":1,"honba":0,"kyotaku":0,"oya":0,"scores":[25000,25000,25000,25000],"tehais":[["E","6p","9m","8m","C","2s","7m","S","6m","1m","S","3s","8m"],["?","?","?","?","?","?","?","?","?","?","?","?","?"],["?","?","?","?","?","?","?","?","?","?","?","?","?"],["?","?","?","?","?","?","?","?","?","?","?","?","?"]]},{"type":"tsumo","actor":0,"pai":"1m"}]
[{"type":"dahai","actor":0,"pai":"C","tsumogiri":false},{"type":"tsumo","actor":1,"pai":"?"},{"type":"dahai","actor":1,"pai":"3m","tsumogiri":false},{"type":"tsumo","actor":2,"pai":"?"},{"type":"dahai","actor":2,"pai":"1m","tsumogiri":false}]
[{"type":"tsumo","actor":3,"pai":"?"},{"type":"dahai","actor":3,"pai":"1m","tsumogiri":false}]
[{"type":"tsumo","actor":0,"pai":"C"}]
EOF
    # ヒアドキュメントの終了マーカー 'EOF' は必ず行頭に記述してください
fi

# --- 後片付け (ボット終了後に実行される) ---
echo "Bot execution finished. Stopping container..."
# スクリプトが終了したらコンテナを停止（--rm オプションで自動削除される）
docker stop $CONTAINER_ID

echo "Done."
