import httpx


async def send_push_notification(title: str, message: str,sender:str,topic:str):



    if not topic:
        print("Nie wysłano powiadomienia: Brak NTFY_TOPIC w pliku .env")
        return False

    url = f"https://ntfy.sh/{topic}"

    title = f"subject : {title} ||| sender : {sender[:25]}"

    headers = {
        "Title": title
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, content=message.encode("utf-8"), headers=headers)

            if response.status_code == 200:
                return True
            else:
                return False

    except Exception as e:
        print(f" Błąd wysyłania powiadomienia ntfy: {e}")
        return False