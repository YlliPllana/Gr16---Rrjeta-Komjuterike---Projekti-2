# Gr16---Rrjeta-Komjuterike---Projekti-2
Komunikimi midis pales se serverit dhe klienteve, permes protokollit TCP (Python)
Ky projekt implementon protokollin TCP ku klientët komunikojnë me serverin duke shkëmbyer komanda dhe përgjigje. Serveri menaxhon lidhjet e klientëve dhe kontrollon aksesin bazuar në privilegjet e secilit klient.

Funksionalitetet e Serverit:
Menaxhimi i Lidhjeve të Klientëve:
Serveri mbështet deri në 4 lidhje të njëkohshme me klientë.
Klienti i parë që lidhet merr akses të plotë dhe ka mundësinë të përdorë të gjitha funksionalitetet e serverit.
Klientët e tjerë që lidhen kanë privilegje të kufizuara, duke pasur akses vetëm për lexim të fajllave.
Komandat e Lejuara për Klientët

Komandat për Klientët me Akses të Plotë:
GET FILES: Liston të gjitha fajllet e disponueshme në SERVER_FILES_DIR.
READ FILE <filename>: Hap dhe lexon përmbajtjen e një fajlli të specifikuar nga SERVER_FILES_DIR.
EXEC CREATE <filename>: Krijon një fajll të ri në SERVER_FILES_DIR.
EXEC LIST: Shfaq listën e klientëve të lidhur aktualisht dhe privilegjet e tyre.
WRITE <filename> <text>: Shkruan tekstin e dhënë në fajllin e përzgjedhur.

Komandat për Klientët me Akses të Kufizuar:
GET FILES: Shfaq një mesazh që tregon kufizimin e aksesit për listimin e fajlleve.
READ FILE <filename>: Lexon përmbajtjen e një fajlli të dhënë, nëse ai ekziston në SERVER_FILES_DIR.

Kerkesat

Serveri
1. Të vendosen variabla te cilat përmbajnë numrin e portit (numri i portit të jetë i
çfarëdoshëm) dhe IP adresën;
2. Të jetë në gjendje të dëgjojë (listën) të paktën të gjithë anëtaret e grupit. Nëse numri i
lidhjeve kalon një prag të caktuar, serveri duhet të refuzojë lidhjet e reja ose t'i vë në pritje;
3. Të menaxhojë kërkesat e pajisjeve që dërgojnë request (ku secili anëtar i grupit duhet
ta ekzekutojë të paktën një kërkesë në server) dhe t’i logojë të gjitha për auditim të
mëvonshëm, duke përfshirë timestamp dhe IP-në e dërguesit;
4. Të jetë në gjendje të lexoje mesazhet që dërgohen nga klientët dhe t’i ruajë për monitorim;
5. Nëse një klient nuk dërgon mesazhe brenda një periudhe të caktuar kohe, serveri duhet ta
mbyllë lidhjen dhe të jetë në gjendje ta rikuperojë atë automatikisht nëse klienti rifutet;
6. Të jetë në gjendje të jap qasje të plotë të paktën njërit klient për qasje në folderat/
përmbajtjen në file-t në server.


Klienti
1. Të krijohet socket lidhja me server;
2. Njëri nga pajisjet (klientët) të ketë privilegjet write(), read(), execute() (qasje të plotë;
execute() përfshin ekzekutimin e komandave të ndryshme në server);
3. Klientët tjerë të kenë vetëm read() permission;
4. Të behet lidhja me serverin duke përcaktuar saktë portin dhe IP Adresën e serverit;
5. Të definohen saktë socket-at e serverit dhe lidhja të mos dështojë;
6. Të jetë në gjendje të lexojë përgjigjet që i kthehen nga serveri;
7. Të dërgojë mesazh serverit në formë të tekstit;
8. Të ketë qasje të plotë në folderat/përmbajtjen në server;
9. Klientët me privilegje të plota të kenë kohë përgjigjeje më të shpejtë se klientët e tjerë që
kanë vetëm read permission.



Punuan:Rina Halili,Yll Jupolli,Ylli Pllana,Yllka Kastrati
