# SAM_Zaoczni_2017_shared

Struktura repozytorium:
- katalog "Docs" -> dokumentacja protokołu + przykładowe pliki
- katalog "Client" -> minimalna implementacja klienta, potrzebna do realizacji zadania
- katalog "Server" -> przykładowa, minimalna implementacja serwera WebSocket (python)

KOD PROGRAMU DO ZREAZLIZOWANIA ZADANIA Z PRZEDMIOTU SIECIOWE APLIKACJE MULTIMEDIALNE


Katalog Client:
- implementacja klienta gry
- możliwość modyfikacji położenia graczy, pocisków, ścian i eksplozji (położenie eksplozji musi być ustawiana po stronie serwera)
- plik SAM_game_min - gra właściwa
- plik minimal_start - tester połączenia z serwerem i wykorzystania protokołu JSON
- sugerowane uruchamianie z wykorzystaniem lokalnego serwera http 
- w katalogu Client wykonać polecenie python -m http.server 8070 LUB python -m SimpleHTTPServer 8070


Katalog Server:
- przykładowa, minimalna implementacja serwera gry z wykorzystaniem języka Python
- pozwala na przesyłanie danych z wykorzystaniem JSON
- polecenie uruchamiające: python Server\SimpleWebSocketServer\SimpleGameServer.py
- domyślny port to 8090, zmienia się go opcją --port numer_portu
- możliwość uruchomienia w trybie echo opcją --example echo
- domyślny protokół to niezabezpieczony HTTP