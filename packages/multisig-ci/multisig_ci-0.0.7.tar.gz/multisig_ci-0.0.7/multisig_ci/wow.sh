export TELEGRAM_MESSAGE=$(cat << EOF
✍️ [eth #1643](https://gnosis-safe.io/app/eth:0x16388463d60FFE0661Cf7F1f31a7D658aC790ff7/transactions/queue) \`"ops: adjust frax vault deposit limit"\`
Sender: "charlesndalton"
Description: \`"Empty Description 🤡"\`
Review [the code](https://github.com/yearn/strategist-ms/pull/1803/files), verify [the output](https://github.com/yearn/strategist-ms/actions/runs/2208972622), and [sign here](https://gnosis-safe.io/app/eth:0x16388463d60FFE0661Cf7F1f31a7D658aC790ff7/transactions/queue)
EOF
)
echo "TELEGRAM_MESSAGE<<EOF" 
echo "$TELEGRAM_MESSAGE"

python3 -m multisig_ci send_and_pin_message 5216969417:AAEcqNoNTgjntgZIzzxCmPNhViR7hV7E7tQ -637585930