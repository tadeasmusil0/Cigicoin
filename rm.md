# Cigicoin
## Ukázka, jak to funguje

### 1. Webová stránka pro zkoušení
Když si v prohlížeči otevřete adresu serveru, naběhne tahle stránka s tlačítky. Přes ně se dá celý blockchain ovládat a zkoušet.

### 2. Jak poslat transakci
Pokud chceme poslat nějaké mince, použijeme část **POST `/transaction`**.
1. Klikneme na **"Try it out"**.
2. Do toho textového pole se přepíše, kdo komu kolik posílá (ve formátu JSON).
3. Potvrdíme to tlačítkem **"Execute"**. Transakce pak čeká ve frontě, než se zapíše do bloku.

![Příprava transakce](image-2.png)
![Odeslání transakce](image-3.png)

### 3. Těžení bloku
Aby se ty transakce z fronty opravdu uložily, musíme blok "vytěžit" (vytvořit).
1. V sekci **GET `/mine`** klikneme na **"Try it out"**.
2. Dáme **"Execute"**. V tu chvíli počítač vypočítá hash a přidá nový blok do řetězce.


### 4. Výpis všech bloků
Celou historii blockchainu si můžeme prohlédnout na adrese `http://127.0.0.1:8000/blocks`. 
Tady je vidět, jak jsou bloky za sebou a jak každý z nich drží hash toho minulého, aby to na sebe sedělo.

![Výpis bloků](image-7.png)

Když budeme těžit dál, budou se prostě přidávat další bloky za sebe do historie.
![Rozšířený blockchain](image-8.png)
