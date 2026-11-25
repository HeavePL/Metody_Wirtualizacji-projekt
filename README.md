# METODY WIRTUALIZACJI - PROJEKT

## 10. Ewidencja godzin pracy

### Struktura JSONA

1. endpoint get(/logs)

    ``` Powershell
    curl.exe -X GET "http://localhost:8080/api/logs"
    ```

    ``` YAML
    logs:
        log:
            id: int
            first_name: str
            last_name: str
            date: str
            start_hour: str
            end_hour: str
            description: str
    ```

2. endpoint get(/log/{id})

    ``` Powershell
    curl.exe -X GET "http://localhost:8080/api/log/3"
    ```

    ``` YAML
    id: int
    first_name: str
    last_name: str
    date: str
    start_hour: str
    end_hour: str
    description: str
    ```

3. endpoint get(/health)

    ``` Powershell
    curl.exe -X GET "http://localhost:8080/api/health"
    ```

    ``` YAML
    status: ok
    ```

4. endpoint post(/logs)

    ``` Powershell
    curl.exe -X POST "http://localhost:8080/api/logs" -H "Content-Type: application/json" -d "{\"first_name\":\"Jan\",\"last_name\":\"Testowy\",\"date\":\"2026-11-26\",\"start_hour\":\"10:00\",\"end_hour\":\"11:00\",\"description\":\"Test\"}"
    ```

    TO

    ``` YAML
    first_name: str
    last_name: str
    date: str
    start_hour: str
    end_hour: str
    description: str
    ```

    RETURN

    ``` YAML
    id: int
    message: "Zapisano pomyślnie"
    ```

5. endpoint delete(/log/{id})

    ``` Powershell
    curl.exe -X DELETE "http://localhost:8080/api/log/6"
    ```

    SUKCES

    ``` YAML
    id: int
    message: "Usunięto pomyślnie"
    ```

    BŁĄD

    ``` YAML
    detail: "Log nie istnieje"
    ```
