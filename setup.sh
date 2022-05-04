mkdir -p ~/.streamlit/
echo "[theme]
primaryColor='#D84727'
backgroundColor='#CDEDF6'
secondaryBackgroundColor='#5EB1BF'
textColor = '#042A2B'
font = 'sans serif'
[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml