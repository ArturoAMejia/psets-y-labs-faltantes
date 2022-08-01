-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Comenzando con la búsqueda de crime_scene_reports como sugiere el pset
SELECT id,description FROM crime_scene_reports WHERE (year = 2021 AND day = 28 AND month = 7 AND street = "Humphrey Street");
-- comprobando las entrevistas desde el día del robo
SELECT id,name,transcript FROM interviews WHERE (year = 2021 AND day = 28 AND month = 7);
-- consultando el cajero automático de LEGGETT STREET para ver los retiros antes de las 10:15 a. m.
SELECT account_number FROM atm_transactions WHERE (year = 2021 AND month = 7 AND day = 28 AND atm_location ="Leggett Street" AND transaction_type = "withdraw");
-- Conecta los números de cuenta bancaria de ese día
SELECT name, phone_number, passport_number, license_plate FROM people WHERE id IN
    (SELECT person_id FROM bank_accounts WHERE account_number IN
    (SELECT account_number FROM atm_transactions WHERE
    (year = 2021 AND month = 7 AND day = 28 AND atm_location ="Leggett Street" AND transaction_type = "withdraw")));
-- Verificando las imágenes de seguridad
SELECT license_plate FROM bakery_security_logs WHERE (year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute <= 25 AND minute >= 15 AND activity = "exit");
-- Comprobar las placas de las personas que retiraron dinero
SELECT name, phone_number, passport_number FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN
(SELECT account_number FROM atm_transactions
WHERE (year = 2021 AND month = 7 AND day = 28 AND atm_location ="Leggett Street"
 AND transaction_type = "withdraw"))) AND license_plate IN
 (SELECT license_plate FROM bakery_security_logs
 WHERE (year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute <= 25 AND minute >= 15 AND activity = "exit"))
  AND phone_number IN (SELECT caller FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60)
  -- Ahora compare los pasaportes con los que tomaron el primer vuelo al día siguiente
SELECT id , passports from flights where year = 2021 and month = 7 and day = 29 order by hour LIMIT1;
  -- Luego compare todo para obtener el nombre de nuestro ladrón
  SELECT name, phone_number FROM people WHERE id IN
    (SELECT person_id FROM bank_accounts WHERE account_number IN
    (SELECT account_number FROM atm_transactions WHERE
    (year = 2021 AND month = 7 AND day = 28 AND atm_location ="Leggett Street" AND transaction_type = "withdraw")))
    AND license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE
    (year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute <= 25 AND minute >= 15 AND activity = "exit"))
    AND phone_number IN (SELECT caller FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60)
    AND passport_number IN (SELECT passport_number FROM passengers
    WHERE flight_id = (SELECT id FROM flights WHERE year = 2021 AND month = 7 AND day = 29 ORDER BY HOUR LIMIT 1));
    --- El ladron es Bruce
    ---Se obtiene el aeropuerto
    SELECT city FROM airports WHERE id IN (SELECT destination_airport_id FROM flights WHERE origin_airport_id = 8 AND year = 2021 AND month = 7 AND day = 29 ORDER BY HOUR LIMIT 1);
    ----La cuidad es New York
    ----Comparo el numero a quien llamó
    SELECT name FROM people WHERE phone_number IN (SELECT receiver FROM phone_calls WHERE caller = "(367) 555-5533"
    AND year = 2021 AND month = 7 AND day = 28 AND duration < 60);
    --- El complice es Robin
