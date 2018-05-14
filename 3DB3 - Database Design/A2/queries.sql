-----------------------------------------------
-- q1)
-----------------------------------------------

SELECT BusID, Age, Manufacturer 
FROM Bus
WHERE AdvertisingRevenue > 9000;


-----------------------------------------------
-- q2)
-----------------------------------------------

SELECT COUNT(SIN)
FROM 	(SELECT SIN
		FROM Person
		WHERE Occupation = 'student' or DateOfBirth > '1992-11-02');


-----------------------------------------------
-- q3)
-----------------------------------------------

SELECT COUNT(SIN)
FROM 	(SELECT SIN 
		FROM Take t
		WHERE t.SIN IN (SELECT SIN
						FROM Person
						WHERE Occupation = 'student' or DateOfBirth > '1992-11-02')
				and t.BusID IN (SELECT B.BusID
								FROM Bus B
								WHERE B.RouteID = 5) and t.date = '2017-05-03');


-----------------------------------------------
-- q4)
-----------------------------------------------

SELECT RouteID, SUM(AdvertisingRevenue) as total
FROM 	(SELECT R.RouteID, B.AdvertisingRevenue
		FROM Route R, Bus B
		WHERE B.RouteID = R.RouteID)
GROUP BY RouteID
ORDER BY total DESC;


-----------------------------------------------
-- q5) (a)
-----------------------------------------------

SELECT P.SIN, FirstName, LastName
FROM Person P, Driver D
WHERE D.SIN NOT IN 	(SELECT SIN
					FROM	(SELECT SIN, SUM(Infraction) as total
							FROM 	(SELECT D.SIN, 1 as Infraction
									FROM Infraction I, Driver D
									WHERE I.SIN = D.SIN)
							GROUP BY SIN)
					WHERE total >= 3) and P.SIN = D.SIN;


-----------------------------------------------
-- q5) (b)
-----------------------------------------------

SELECT * 
FROM	(SELECT SIN, SUM(DEMERIT) as total_demerit, SUM(FINE) as total_fine
		FROM 	(SELECT D.SIN, Demerit, Fine
				FROM Infraction I, Driver D
				WHERE I.SIN = D.SIN)
		GROUP BY SIN
		ORDER BY total_demerit DESC, total_fine DESC)
WHERE total_demerit >= 2;


-----------------------------------------------
-- q6)
-----------------------------------------------

SELECT BusID, B.Manufacturer
FROM Bus B, (SELECT Manufacturer
			FROM	(SELECT COUNT(BusID) as count, Manufacturer
					FROM	(SELECT BusID, Manufacturer
							FROM Bus)
					GROUP BY Manufacturer)
			WHERE count = 1) X
WHERE B.Manufacturer = X.Manufacturer;


---------------------------------------------
-- q7) (a)
---------------------------------------------

SELECT Type, SUM(Fee) as TOTAL_FARE_REVENUE
FROM	(SELECT P.Type, F.Fee
		FROM Take T, Passenger P, Fare F
		WHERE T.SIN = P.SIN and P.Type = F.Type)
GROUP BY Type;


---------------------------------------------
-- q7) (b)
---------------------------------------------

SELECT *
FROM	(SELECT Type, SUM(Fee) as TOTAL_FARE_REVENUE
		FROM	(SELECT P.Type, F.Fee
				FROM Take T, Passenger P, Fare F
				WHERE T.SIN = P.SIN and P.Type = F.Type)
		GROUP BY Type)
WHERE TOTAL_FARE_REVENUE > 500;


---------------------------------------------
-- q7) (c)
---------------------------------------------

SELECT *
FROM	(SELECT Type, SUM(Fee) as TOTAL_FARE_REVENUE
		FROM	(SELECT P.Type, F.Fee
				FROM Take T, Passenger P, Fare F
				WHERE T.SIN = P.SIN and P.Type = F.Type)
		GROUP BY Type
		ORDER BY TOTAL_FARE_REVENUE DESC)
FETCH FIRST 1 ROWS ONLY;


---------------------------------------------
-- q8) (a)
---------------------------------------------

SELECT RouteID, SUM(count) as TOTAL_PASSENGERS
FROM	(SELECT RouteID, 1 as count
		FROM Bus B, Take T
		WHERE B.BusID = T.BusID and T.Date = '2017-05-07')
GROUP BY RouteID
ORDER BY TOTAL_PASSENGERS DESC
FETCH FIRST 1 ROWS ONLY;


---------------------------------------------
-- q8) (b)
---------------------------------------------

SELECT Date, SUM(count) as TOTAL_PASSENGERS
FROM 	(SELECT T.Date, 1 as count
		FROM Bus B, Take T
		WHERE B.BusID = T.BusID)
GROUP BY Date
ORDER BY TOTAL_PASSENGERS DESC
FETCH FIRST 1 ROWS ONLY;


---------------------------------------------
-- q9)
-- I will consider that a person visited a 
-- library if they rode a bus route that 
-- goes to any sites of type library.
---------------------------------------------

SELECT P.SIN, P.Occupation
FROM Person P, Take T, Bus B
WHERE B.RouteID IN 	(SELECT DISTINCT R.RouteID
					FROM Route R, Go G, Sites S
					WHERE R.RouteID = G.RouteID and G.SIName = S.SIName and S.Category = 'Library')
					and P.SIN = T.SIN and T.BusID = B.BusID and (T.Date = '2017-05-06' or T.date = '2017-05-07');


---------------------------------------------
-- q10)
---------------------------------------------

SELECT P.FirstName, P.LastName, D.SIN
FROM Driver D, Person P
Where D.SIN = P.SIN and D.SIN IN 	(SELECT SIN
									FROM 	(SELECT SIN, SUM(DEMERIT) as total_demerit
											FROM 	(SELECT D.SIN, Demerit, D.YearsOfService, D.Salary
													FROM Infraction I, Driver D
													WHERE I.SIN = D.SIN)
											GROUP BY SIN)
									WHERE total_demerit < 10 and D.YearsOfService > 5 and D.Salary > 80000);


---------------------------------------------
-- q11)
-- I will assume that a student attended the 
-- tennis match if they rode a route 4 bus
-- on that day and before the start time of 
-- the event.
---------------------------------------------

SELECT P.FirstName, P.LastName, P.Sex
FROM Person P, Take T, Bus B
WHERE P.SIN IN 	(SELECT SIN
				FROM Person
				WHERE Occupation = 'student' or DateOfBirth > '1992-11-02')
				and B.RouteID = 4 and P.SIN = T.SIN and T.BusID = B.BusID and T.Date = '2017-05-02' and T.Time < '18:15:00';


---------------------------------------------
-- q12)
---------------------------------------------

SELECT DISTINCT R.RouteID
FROM Route R, Schedule Sc, Stop St, Sites Si
WHERE R.RouteID = Sc.RouteID and Sc.Date = '2017-05-01' and Sc.StopID = St.StopID and St.SIName = Si.SIName and Si.SIName = 'Ron Joyce Stadium' and Sc.ArrivalTime >= '16:20:00' and Sc.ArrivalTime <= '16:50:00';

