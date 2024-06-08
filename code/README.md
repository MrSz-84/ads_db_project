___
# Design Document

By Marcin Borowski


GitHub repo: [repository](https://github.com/MrSz-84/ads_db_project)

<br>

## Scope

This project was designed and executed to serve few purposes:

1. As a learning process of databases data manipulation and communication with database via python api.
2. A place to store data about radio, television and display advertisements emitted by companies on AGD RTV market retail in Poland.
3. As fast and reliable place to write to and read from for reporting purposes. Storing this data in Excel files is deeming, slow and prone to data loss.
4. As learning experience for Pandas package usage, ways of data manipulation and aggregation.
5. A way of automating tedious and repetitive work.

This project consists of 3 different databases based on Sqlite3 engine and syntax, in tandem with sqlite3 module build in Python itself. 
Unfortunately the DBAPI is quite a few updates behind the DB engine, thus I was unable tu utilize all of its new features.

1. Radio ads database:
   * The database is storing data gathered by the company conducting market surveys of television advertisement (Kantar Media).
   * There are few main companies which own radio stations of various reach across Poland, and each radio station can broadcast radio ads.
   * It *includes*, radio brand owners, radio brands, radio stations, brands instructing ads broadcasting, exact days, hours, dayparts, lengths, and simple transcriptions of ad contents.
   * Contents of those ads also *includes* other brands and manufacturers of commodities.
2. TV ads database:
   * The database is storing data gathered by the company conducting market surveys of radio advertisement (Nielsen).
   * There are few main companies which own tv stations of nationwide reach across Poland, and each tv owner can broadcast tv ads on multiple television channels.
   * It *includes*, tv channels and channel groups, brands instructing ads broadcasting, exact days, hours, dayparts, lengths, and simple transcriptions of ad contents.
   * Contents of those ads also *includes* other brands and manufacturers of commodities.
3. Display ads on main www sites in Poland.
   * The database is storing data gathered by hand surveying during daily checks.
   * It contains only display online ads, capped or bought in FF mode.
   * All CPM campaigns, GAds, RTB and similar advertisements are excluded from this dataset.
   * Data indicates the site on which ad was placed, date, name of the ad slot, who instructed the ad and avg. ad impressions.

<br>

> **NOTE**
>
> Code used in creation of functions and triggers is written using SQL and Sqlite 3 syntax, so it may have some quirks. Please keep this in mind.

<br>

## Functional Requirements

The database is going to help with:

* Storing the data of radio, tv and display ads for given branch of Polish retail market.
* Providing updates of the data in continuous manner. Reporting is conducted usually in daily manner.
* Enabling data edition and correction using SQL syntax and the benefits of transactions.
* Creation of reports, tables, charts, analysis etc.
* Reading the data to other environments such as Power BI, Pandas, Matplotlib, or simply providing tables in pure SQL queries.
* Conducting various data read and write duration tests.
* Reduction of disk space needed to store data in Excel files. Microsoft's Excel team knows how to compress the data, but good data model can save a lat of space!


## Representation
The data is being transferred into SQL tables as mentioned below. I used snowflake type data models in tv and radio ads, and star type data model in display ads DB. 
The fact tables are named spoty in both, the tv and radio advertisements DB, and placementy in display ads DB. Rest of the tables are considered as dimension ones.

### Entities


#### <u>Radio ads database fact table `spoty`</u>

The `spoty` table contains the data about the advertisement emission, their contents, type, code, 
who instructed the broadcast, where it was broadcast, ad emission time details, costs etc. 
The smallest unit of this table is one emission. Each row must have entries in all columns 
except one (`koszt`), therefor `NOT NULL` constraints were added. Columns included in this table are:

- `id` which is the unique identification number of each ad emission, and by so has `PRIMARY KEY` 
constraint applied.
- `data` which states when given emission took place. Date is in ISO 8601 format. In addition, 
this is the column which relates to `data_czas` table, thus `FOREIGN KEY` constraints were applied.
- `gg` which is the hour at which the emission took place. `INTEGER` data type was used here.
- `mm` which is the minute ow an hour at which the emission took place. `INTEGER` data type was used
here.
- `ss` which is the second ow a minute at which the emission took place. `INTEGER` data type was used
here.
- `koszt` which represents the rate card cost of single emission. Best fit for rate card costs, 
being whole numbers is `INTEGER` type. This field can be empty, so no constraints was added.
- `dlugosc` is the actual duration time of a single spot emission. 
- `kod_rek_id` which should be a unique numeric value of given advertisement. 
The type `INTEGER` was used here, cuz this field represents a `FOREIGN KEY` to a dimension table 
containing actual code value. 

    > **NOTE!**
    > 
    > ADVERTISEMENT != EMISSION 
    > 
    > The same advertisement can be emitted several times.


- `daypart_id` which is a unique number that can be bound with the information about which daypart 
this spot was emitted. Daypart is an arbitrary value addressing company reporting needs.
- `dl_ujednolicona_id` which is a unique number that can be bound to a dimension table representing
unified lengths of distinct ad spot. Those lengths being (in seconds): 10, 15, 20, 30, 45, 60.
- `blok_rek_id` this is a range of 30 minutes in which advertising spots must be emitted. 
A brand instructing emission can choose how many and in which slot ads must appear. 
This is represented as text in GG:MM-GG:MM format, where the first part MM must be either 00 or 30, 
and the second 29 or 59 respectively. This field is a foreign key for the actual string representation 
of the time block, thus  `INTEGER` was used here as a data type, and `FOREIGN KEY` restrictions were added.
- `brand_id` which contains unique number that can be bound with brand instructing the emission 
(ad owner) table. Type used `INTEGER`, and `FOREIGN KEY` restrictions were added.
- `submedium_id` which contains unique number that can be bound with the owner od radio group 
- or single radio station gathered in another table. Type used `INTEGER`, and `FOREIGN KEY` 
restrictions were added.
- `typ_produktu_id` which contains unique number that can be bound with typu_produktow table. 
Thus type `INTEGER` was used and `FOREIGN KEY` constraints applied.
- `l_emisji` is a number of ad emission. This value can't be a negative number, so `CHECK` was added,
and `INTEGER` type used.
- `typ_rek_id` which holds type of add, thus `TEXT` was used as a type, and a `DEFAULT` value set in
case of missing data.

#### <u>TV ads database fact table `spoty`</u>

The `spoty` table contains the data about the advertisement emission, their contents, type, code, 
who instructed the broadcast, where it was broadcast, ad emission time details, costs etc. 
The smallest unit of this table is one emission. Each row must have entries in all columns 
except three (`prog_kampania_id`, `program_przed_id`, `program_po_id`), therefor `NOT NULL` 
constraints were added. Columns included in this table are:

- `id` which is the unique identification number of each ad emission, and by so has `PRIMARY KEY` 
constraint applied.
- `data` which states when given emission took place. Date is in ISO 8601 format. In addition, 
this is the column which relates to `data_czas` table, thus `FOREIGN KEY` constraints were applied.
- `czas` which is the time of emission in ISO format HH:MM:SS, here represented as `TEXT` data type.
- `pib_pos` which represents the numeric position in ad block. Thus `INTEGER` type was used.
- `pib_count` which represents the count of all ad emissions in given ad block. Therefore `INTEGER`
data type was used.
- `pib_real_rel_id` which is a unique numeric representation of a real relative ad in given block.
It can, for instance, take values as *first*, *last*, *second last*, etc.
- `klasa_spotu_id` which is a unique number that can be bound with the information about the type of
every spot sored in dimension table. Here `INTEGER` data type was used.
- `kod_bloku_id` which is a unique number that can be bound with the information about the code of ad
block in which given ad was emitted. Actual  data can be found in dimension table, 
here `FOREIGN KEY` of `INTEGER` data type was used.
- `daypart_id` which is a unique number that can be bound with the information about which daypart 
this spot was emitted. Here, contrary to radio_ads DB, the daypart is an industry standard represented as 
*prime* and *off*. Those are best broadcast times, and those less lucrative in audience. 
- `grp` being the number of gross rating points of particular ad emission. It is a floating point number
therefore `REAL` data type was used.
- `kanal_id` which is a unique number that can be bound with the information about on what channel ad
was emitted. That dimension table contains of chanel name and chanel group that consolidates numerous channels.
- `brand_id` which contains unique number that can be bound with brand instructing the emission 
(ad owner) table. Type used `INTEGER`, and `FOREIGN KEY` restrictions were added.
- `dlugosc_id` which is a unique number that can be bound to a dimension table representing
unified lengths of distinct ad spot. Contrary to radio_ads DB, here industry standards are forced.
- `kod_rek_id` which should be a unique numeric value of given advertisement. 
The type `INTEGER` was used here, cuz this field represents a `FOREIGN KEY` to a dimension table 
containing actual code value. 

    > **NOTE!**
    > 
    > ADVERTISEMENT != EMISSION
    > 
    > The same advertisement can be emitted several times.

- `prog_kampania_id` which is a unique number that can be bound to a dimension table representing
during what tv program given spot was emitted, hence `FOREIGN KEY` as `INTEGER` data type was used here.
- `program_przed_id` which is a unique number that can be bound to a dimension table representing
before what tv program given spot was emitted, hence `FOREIGN KEY` as `INTEGER` data type was used here.
- `program_po_id` which is a unique number that can be bound to a dimension table representing
after what tv program given spot was emitted, hence `FOREIGN KEY` as `INTEGER` data type was used here.


#### <u>Display ads database fact table `placementy`</u>

The `placementy` table contains the data about the advertisement emission, where were they emitted,
at what online placement the ad was seen, when it was emitted, who instructed the broadcast, 
the number of ad impressions etc. 
This is the smallest of all databases in this project, yet the data is sufficient for reporting 
purposes and analysis. All columns need to be filled with data. Columns included in this table are:

- `id` which is the unique identification number of each ad emission, and by so has `PRIMARY KEY` 
constraint applied.
- `data` which states when given emission took place. Date is in ISO 8601 format. In addition, 
this is the column which relates to `data_czas` table, thus `FOREIGN KEY` constraints were applied.
- `wydawca_id` which contains unique number that can be bound with the www site owner, on which 
given ad was emitted.
- `format_id` which contains unique number that can be bound with the format name, which was used for
given ad emission.
- `urzadzenie_id` which contains unique number that can be bound with the type of device, on which
ad could be seen. Those would be desktop, mobile and cross device.
- `brand_id` which contains unique number that can be bound with brand instructing the emission 
(ad owner) table. Type used `INTEGER`, and `FOREIGN KEY` restrictions were added.
- `pv` the number of impression made by given ad emission. These values are estimated based on own 
emissions, and broadcaster data


### Relationships

In the ER diagram below User can find the relationships between tables, as well the identification 
of each used column and its type. Mermaid for VSC was used for creation. See **[Marmaid](https://mermaid.js.org/)** 
website for more information.

<br>
<br>

#### **ER DIAGRAM -> RADIO ADS DB**
```mermaid
---
title: Radio Ads DB powered by Sqlite3
---
erDiagram
    DNI_TYG         ||--|{ DATA_CZAS : has
    MIESIACE        ||--|{ DATA_CZAS : has
    SUBMEDIA        }|--|| NADAWCY : has
    SUBMEDIA        }|--|| ZASIEGI : has
    SPOTY           }|--|| DAYPARTY : is_in
    SPOTY           }|--|| DL_UJEDNOLICONE : is_of
    BRANDY          ||--|{ SPOTY : emitted_by
    SPOTY           }|--|| SUBMEDIA : emitted_via
    DATA_CZAS       ||--|{ SPOTY : took_place
    TYPY_PRODUKTU   ||--|{ SPOTY : is_of
    BLOKI_REK       ||--|{ SPOTY : is_in
    SPOTY           }|--|| KODY_REK : is_of
    TYPY_REK        ||--|{ SPOTY : is_of


    TYPY_PRODUKTU {
    name     typy_produktu
    integer  id
    text     typ_produktu
    }
    DNI_TYG {
    name     dni_tyg
    integer  id
    text     dzien_tyg
    }
    MIESIACE {
    name     miesiace
    integer  id
    text     miesiac
    }
    DATA_CZAS {
    name     data_czas
    integer  id
    text     data
    integer  dzien
    integer  dzien_tyg_nr
    integer  tydzien  
    integer  miesiac_nr
    integer  rok
    }
    SUBMEDIA {
    name     submedia
    integer  id
    text     submedium 
    integer  nadawca_id
    integer  zasieg_id      
    }
    NADAWCY {
    name     nadawcy
    integer  id
    text     nadawca         
    }
    ZASIEGI {
    name     zasiegi
    integer  id
    text     zasieg        
    }
    BRANDY {
    name     brandy
    integer  id
    text     brand     
    }
    DAYPARTY {
    name     dayparty
    integer  id
    text     daypart
    }
    DL_UJEDNOLICONE {
    name     dl_ujednolicone
    integer  id
    integer  dl_ujednolicona
    }
    BLOKI_REK {
    name     bloki_rek
    integer  id
    text     blok_rek
    }
    KODY_REK {
    name     kody_rek
    integer  id
    integer  kod_rek
    text     opis
    }
    TYPY_REK { 
    name     typy_rek
    integer  id
    text     typ_rek
    }
    SPOTY {
    name     spoty
    integer  id
    text     data
    integer  gg
    integer  mm
    integer  ss
    integer  koszt
    integer  dlugosc
    integer  kod_rek_id
    integer  daypart_id
    integer  dl_ujednolicona_id
    integer  blok_rek_id
    integer  brand_id
    integer  submedium_id
    integer  typ_produktu_id
    integer  l_emisji
    integer  typ_rek_id
    }
```

<br><br>

#### **ER DIAGRAM -> TV ADS DB**
```mermaid
---
title: TV Ads DB powered by Sqlite3
---
erDiagram
    DNI_TYG         ||--|{ DATA_CZAS : has
    MIESIACE        ||--|{ DATA_CZAS : has
    KANALY          }|--|| KANALY_GR : in
    SPOTY           }|--|| DAYPARTY : is_in
    SPOTY           }|--|| DLUGOSCI : is_of
    BRANDY          ||--|{ SPOTY : emitted_by
    PRODUCERS       ||--|| BRANDY: produced_by
    SYNDICATES      ||--|| BRANDY: govern_by
    SPOTY           }|--|| KANALY : emitted_via
    DATA_CZAS       ||--|{ SPOTY : took_place
    KODY_BLOKU      ||--|{ SPOTY : is_in
    SPOTY           }|--|| KODY_REK : is_of
    KLASY_SPOTU     }|--|| SPOTY : is_of
    SPOTY           ||--|{ PIB_REAL_RELS: at_place
    SPOTY           }|--|| PROG_KAMPANIE: during
    SPOTY           }|--|| PROGRAMY_PO: after
    PROGRAMY_PRZED  }|--|| SPOTY: before



    DNI_TYG {
    name     dni_tyg
    integer  id
    text     dzien_tyg
    }
    MIESIACE {
    name     miesiace
    integer  id
    text     miesiac
    }
    DATA_CZAS {
    name     data_czas
    integer  id
    text     data
    integer  dzien
    integer  dzien_tyg_nr
    integer  tydzien  
    integer  miesiac_nr
    integer  rok
    }
    KODY_REK {
    name     kody_rek
    integer  id
    integer  kod_rek
    text     opis
    }
    PRODUCERS { 
    name     producers
    integer  id
    text     producer
    }
    SYNDICATES { 
    name     syndicates
    integer  id
    text     syndicate
    }
    BRANDY {
    name     brandy
    integer  id
    text     brand
    integer  producer_id
    integer  syndicate_id
    }
    KANALY_GR { 
    name     kanaly_gr
    integer  id
    text     kanal_gr
    }
    KANALY {
    name     kanaly
    integer  id
    text     kanal
    integer  kanal_gr_id
    }
    DAYPARTY {
    name     dayparty
    integer  id
    text     daypart
    }
    PIB_REAL_RELS {
    name     pib_real_rels
    integer  id
    text     pib_real_rel
    }
    DLUGOSCI {
    name     dlugosci
    integer  id
    integer  dlugosc
    }
    KLASY_SPOTU {
    name     klasy_spotu
    integer  id
    text     klasa_spotu        
    }
    KODY_BLOKU {
    name     kody_bloku
    integer  id
    text     kod_bloku
    }
    PROG_KAMPANIE {
    name     prog_kampanie
    integer  id
    text     prog_kampania
    }
    PROGRAMY_PRZED {
    name     programy_przed
    integer  id
    text     program_przed
    }
    PROGRAMY_PO {
    name     programy_po
    integer  id
    text     program_po
    }
    SPOTY {
    name     spoty
    integer  id
    text     data
    text     czas
    integer  pib_pos
    integer  pib_count
    integer  pib_real_rel_id
    integer  klasa_spotu_id
    integer  kod_bloku_id
    integer  daypart_id
    real     grp
    integer  kanal_id
    integer  brand_id
    integer  dlugosc_id
    integer  kod_rek_id
    integer  prog_kampania_id
    integer  program_przed_id
    integer  program_po_id
    }
```

<br><br>

#### **ER DIAGRAM -> DISPLAY ADS DB**
```mermaid
---
title: Display Ads DB powered by Sqlite3
---
erDiagram
    DNI_TYG         ||--|{ DATA_CZAS : has
    MIESIACE        ||--|{ DATA_CZAS : has
    BRANDY          ||--|{ PLACEMENTY : emitted_by
    DATA_CZAS       ||--|{ PLACEMENTY : took_place
    WYDAWCY         ||--|{ PLACEMENTY : emitted_on
    PLACEMENTY      }|--|| FORMATY: of_type
    PLACEMENTY      }|--|| URZADZENIA: device_type


    MIESIACE {
    name     miesiace
    integer  id
    text     miesiac
    }
    DNI_TYG {
    name     dni_tyg
    integer  id
    text     dzien_tyg
    }
    DATA_CZAS {
    name     data_czas
    integer  id
    text     data
    integer  dzien
    integer  dzien_tyg_nr
    integer  tydzien  
    integer  miesiac_nr
    integer  rok
    }
    WYDAWCY {
    name     wydawcy
    integer  id
    text     wydawca
    }
    FORMATY { 
    name     formaty
    integer  id
    text     format
    }
    BRANDY {
    name     brandy
    integer  id
    text     brand
    }
    URZADZENIA { 
    name     urzadzenia
    integer  id
    text     urzadzenie
    }
    PLACEMENTY {
    name     placementy
    integer  id
    text     data
    integer  wydawca_id
    integer  format_id
    integer  urzadzenie_id
    integer  brand_id
    integer  pv
    }
```