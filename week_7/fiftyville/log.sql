-- Keep a log of any SQL queries you execute as you solve the mystery.

.schema -- To have an idea what data is available.

SELECT id, name FROM people;
SELECT COUNT(name) FROM people;
-- Took a look on how many people are in town.

SELECT id, year, month, day, description FROM crime_scene_reports WHERE street LIKE '%Humphrey%';
-- Looked the history of crimes on Humphrey Street
-- Got info from 28 July 2024: Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
-- Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery.

SELECT id, name, transcript FROM interviews WHERE year = 2024 AND month = 7 AND day = 28;
-- Decided to look at these interviews.
-- Ruth said: Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away.
-- If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.
-- Eugene said: I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery,
-- I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.
-- Raymond said: As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call,
-- I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
-- The thief then asked the person on the other end of the phone to purchase the flight ticket.

-- Lets observe parking lot
SELECT id, activity, license_plate, hour, minute FROM bakery_security_logs WHERE year = 2024 AND month = 7 AND day = 28;
-- Filter results by time
SELECT id, activity, license_plate, hour, minute FROM bakery_security_logs WHERE year = 2024 AND month = 7 AND day = 28 AND hour >= 9 AND hour <= 10;
-- Ruth informs that in an interval of 10 minutes after 10:15 am the suspects car left the parking
SELECT license_plate FROM bakery_security_logs WHERE year = 2024 AND month = 7 AND day = 28 AND hour = 10 AND minute < 25 AND activity = 'exit';
-- There are 8 results of possible suspects car.
-- 5P2BI95, 94KL13X, 6P58WS2, 4328GD8, G412CB7, L93JTIZ, 322W7JE, 0NTHK55

-- Lets check atms
SELECT account_number, transaction_type, amount FROM atm_transactions WHERE year = 2024 AND month = 7 AND day = 28 AND (atm_location LIKE '%Leggett%');
SELECT account_number FROM atm_transactions WHERE year = 2024 AND month = 7 AND day = 28 AND (atm_location LIKE '%Leggett%') AND transaction_type = 'withdraw';
-- 8 possible account numbers:
-- 28500762, 28296815, 76054385, 49610011, 16153065, 25506511, 81061156, 26013199
-- Lets also get suspects person ids by banc account numbers:
SELECT person_id, creation_year FROM bank_accounts WHERE account_number
IN (SELECT account_number FROM atm_transactions WHERE year = 2024 AND month = 7 AND day = 28 AND (atm_location LIKE '%Leggett%') AND transaction_type = 'withdraw');

-- Lets check phone calls
SELECT caller, receiver, duration FROM phone_calls WHERE year = 2024 AND month = 7 AND day = 28;
SELECT caller, receiver FROM phone_calls WHERE year = 2024 AND month = 7 AND day = 28 AND duration < 60;
-- last query returns 8 possible pairs of callers and receivers.

-- Lets get possible suspects by collected info
SELECT name, id FROM people WHERE phone_number IN (SELECT caller FROM phone_calls WHERE year = 2024 AND month = 7 AND day = 28 AND duration < 60)
AND license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE year = 2024 AND month = 7 AND day = 28 AND hour = 10 AND minute < 25 AND activity = 'exit')
AND id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE year = 2024 AND month = 7 AND day = 28 AND (atm_location LIKE '%Leggett%') AND transaction_type = 'withdraw'));
-- We got two options: it's either Diana, 514354 or Bruce, 686048.

-- Lets check airport info for last
SELECT id, abbreviation, full_name FROM airports WHERE city = 'Fiftyville';
SELECT id, destination_airport_id, hour, minute FROM flights WHERE origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville') AND year = 2024 AND month = 7 AND day = 29 ORDER BY hour, minute;
SELECT city, abbreviation, full_name FROM airports WHERE id = (SELECT destination_airport_id FROM flights WHERE origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville') AND year = 2024 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1);
-- It looks like the suspect was going to New York City, LGA, LaGuardia Airport
-- Flight id is:
SELECT id FROM flights WHERE origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville') AND year = 2024 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1;
-- Lets get all passangers:
SELECT passport_number, seat FROM passengers WHERE flight_id = (SELECT id FROM flights WHERE origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville') AND year = 2024 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1);

SELECT name, id FROM people WHERE phone_number IN (SELECT caller FROM phone_calls WHERE year = 2024 AND month = 7 AND day = 28 AND duration < 60)
AND license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE year = 2024 AND month = 7 AND day = 28 AND hour = 10 AND minute < 25 AND activity = 'exit')
AND id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE year = 2024 AND month = 7 AND day = 28 AND (atm_location LIKE '%Leggett%') AND transaction_type = 'withdraw'))
AND passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = (SELECT id FROM flights WHERE origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville') AND year = 2024 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1));
-- Looks like the thief is Bruce, 686048!

-- Lets lastly find out who helped the thief...
SELECT receiver FROM phone_calls WHERE year = 2024 AND month = 7 AND day = 28 AND duration < 60 AND caller = (SELECT phone_number FROM people WHERE id = 686048);
SELECT name, id FROM people WHERE phone_number = (SELECT receiver FROM phone_calls WHERE year = 2024 AND month = 7 AND day = 28 AND duration < 60 AND caller = (SELECT phone_number FROM people WHERE id = 686048));
-- Surely, it's Robin, 864400.
