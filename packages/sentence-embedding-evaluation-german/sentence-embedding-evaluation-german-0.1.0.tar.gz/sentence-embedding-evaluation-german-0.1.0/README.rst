|PyPI version| |Total alerts| |Language grade: Python|

sentence-embedding-evaluation-german
====================================

Sentence embedding evaluation for German.

This library is inspired by
`SentEval <https://github.com/facebookresearch/SentEval>`__ but focuses
on German language downstream tasks.

Downstream tasks
----------------

+---------+---------+---------+---------+---------+---------+---------+
| task    | type    | pro     | #train  | #test   | target  | info    |
|         |         | perties |         |         |         |         |
+=========+=========+=========+=========+=========+=========+=========+
| TOXIC   | 👿      | f       | 3244    | 944     | binary  | G       |
|         | toxic   | acebook |         |         | {0,1}   | ermEval |
|         | c       | c       |         |         |         | 2021,   |
|         | omments | omments |         |         |         | c       |
|         |         |         |         |         |         | omments |
|         |         |         |         |         |         | subtask |
|         |         |         |         |         |         | 1,      |
|         |         |         |         |         |         | `📁 <ht |
|         |         |         |         |         |         | tps://g |
|         |         |         |         |         |         | ithub.c |
|         |         |         |         |         |         | om/germ |
|         |         |         |         |         |         | eval202 |
|         |         |         |         |         |         | 1toxic/ |
|         |         |         |         |         |         | SharedT |
|         |         |         |         |         |         | ask>`__ |
|         |         |         |         |         |         | `📖     |
|         |         |         |         |         |         |  <http  |
|         |         |         |         |         |         | s://acl |
|         |         |         |         |         |         | antholo |
|         |         |         |         |         |         | gy.org/ |
|         |         |         |         |         |         | 2021.ge |
|         |         |         |         |         |         | rmeval- |
|         |         |         |         |         |         | 1.1>`__ |
+---------+---------+---------+---------+---------+---------+---------+
| ENGAGE  | 🤗      | f       | 3244    | 944     | binary  | G       |
|         | e       | acebook |         |         | {0,1}   | ermEval |
|         | ngaging | c       |         |         |         | 2021,   |
|         | c       | omments |         |         |         | c       |
|         | omments |         |         |         |         | omments |
|         |         |         |         |         |         | subtask |
|         |         |         |         |         |         | 2,      |
|         |         |         |         |         |         | `📁 <ht |
|         |         |         |         |         |         | tps://g |
|         |         |         |         |         |         | ithub.c |
|         |         |         |         |         |         | om/germ |
|         |         |         |         |         |         | eval202 |
|         |         |         |         |         |         | 1toxic/ |
|         |         |         |         |         |         | SharedT |
|         |         |         |         |         |         | ask>`__ |
|         |         |         |         |         |         | `📖     |
|         |         |         |         |         |         |  <http  |
|         |         |         |         |         |         | s://acl |
|         |         |         |         |         |         | antholo |
|         |         |         |         |         |         | gy.org/ |
|         |         |         |         |         |         | 2021.ge |
|         |         |         |         |         |         | rmeval- |
|         |         |         |         |         |         | 1.1>`__ |
+---------+---------+---------+---------+---------+---------+---------+
| FCLAIM  | ☝️      | f       | 3244    | 944     | binary  | G       |
|         | fact-c  | acebook |         |         | {0,1}   | ermEval |
|         | laiming | c       |         |         |         | 2021,   |
|         | c       | omments |         |         |         | c       |
|         | omments |         |         |         |         | omments |
|         |         |         |         |         |         | subtask |
|         |         |         |         |         |         | 3,      |
|         |         |         |         |         |         | `📁 <ht |
|         |         |         |         |         |         | tps://g |
|         |         |         |         |         |         | ithub.c |
|         |         |         |         |         |         | om/germ |
|         |         |         |         |         |         | eval202 |
|         |         |         |         |         |         | 1toxic/ |
|         |         |         |         |         |         | SharedT |
|         |         |         |         |         |         | ask>`__ |
|         |         |         |         |         |         | `📖     |
|         |         |         |         |         |         |  <http  |
|         |         |         |         |         |         | s://acl |
|         |         |         |         |         |         | antholo |
|         |         |         |         |         |         | gy.org/ |
|         |         |         |         |         |         | 2021.ge |
|         |         |         |         |         |         | rmeval- |
|         |         |         |         |         |         | 1.1>`__ |
+---------+---------+---------+---------+---------+---------+---------+
| VMWE    | verbal  | ne      | 6652    | 1447    | binary  | G       |
|         | idioms  | wspaper |         |         | (figura | ermEval |
|         |         |         |         |         | tively, | 2021,   |
|         |         |         |         |         | lit     | verbal  |
|         |         |         |         |         | erally) | idioms, |
|         |         |         |         |         |         | `       |
|         |         |         |         |         |         | 📁 <htt |
|         |         |         |         |         |         | ps://gi |
|         |         |         |         |         |         | thub.co |
|         |         |         |         |         |         | m/rafeh |
|         |         |         |         |         |         | r/vid-d |
|         |         |         |         |         |         | isambig |
|         |         |         |         |         |         | uation- |
|         |         |         |         |         |         | sharedt |
|         |         |         |         |         |         | ask>`__ |
|         |         |         |         |         |         | `📖 <h  |
|         |         |         |         |         |         | ttps:// |
|         |         |         |         |         |         | aclanth |
|         |         |         |         |         |         | ology.o |
|         |         |         |         |         |         | rg/2020 |
|         |         |         |         |         |         | .figlan |
|         |         |         |         |         |         | g-1.29. |
|         |         |         |         |         |         | pdf>`__ |
+---------+---------+---------+---------+---------+---------+---------+
| OL19-A  | 👿      | tweets  | 3980    | 3031    | binary  | G       |
|         | of      |         |         |         | {0,1}   | ermEval |
|         | fensive |         |         |         |         | 2018,   |
|         | l       |         |         |         |         | `📁 <h  |
|         | anguage |         |         |         |         | ttps:// |
|         |         |         |         |         |         | project |
|         |         |         |         |         |         | s.fzai. |
|         |         |         |         |         |         | h-da.de |
|         |         |         |         |         |         | /iggsa/ |
|         |         |         |         |         |         | data-20 |
|         |         |         |         |         |         | 19/>`__ |
|         |         |         |         |         |         | `📖 <   |
|         |         |         |         |         |         | https:/ |
|         |         |         |         |         |         | /corpor |
|         |         |         |         |         |         | a.lingu |
|         |         |         |         |         |         | istik.u |
|         |         |         |         |         |         | ni-erla |
|         |         |         |         |         |         | ngen.de |
|         |         |         |         |         |         | /data/k |
|         |         |         |         |         |         | onvens/ |
|         |         |         |         |         |         | proceed |
|         |         |         |         |         |         | ings/pa |
|         |         |         |         |         |         | pers/ge |
|         |         |         |         |         |         | rmeval/ |
|         |         |         |         |         |         | GermEva |
|         |         |         |         |         |         | lShared |
|         |         |         |         |         |         | Task201 |
|         |         |         |         |         |         | 9Iggsa. |
|         |         |         |         |         |         | pdf>`__ |
+---------+---------+---------+---------+---------+---------+---------+
| OL19-B  | 👿      | tweets  | 3980    | 3031    | 4 catg. | G       |
|         | of      |         |         |         | (pro    | ermEval |
|         | fensive |         |         |         | fanity, | 2018,   |
|         | la      |         |         |         | insult, | `📁 <h  |
|         | nguage, |         |         |         | abuse,  | ttps:// |
|         | fine-   |         |         |         | oth.)   | project |
|         | grained |         |         |         |         | s.fzai. |
|         |         |         |         |         |         | h-da.de |
|         |         |         |         |         |         | /iggsa/ |
|         |         |         |         |         |         | data-20 |
|         |         |         |         |         |         | 19/>`__ |
|         |         |         |         |         |         | `📖 <   |
|         |         |         |         |         |         | https:/ |
|         |         |         |         |         |         | /corpor |
|         |         |         |         |         |         | a.lingu |
|         |         |         |         |         |         | istik.u |
|         |         |         |         |         |         | ni-erla |
|         |         |         |         |         |         | ngen.de |
|         |         |         |         |         |         | /data/k |
|         |         |         |         |         |         | onvens/ |
|         |         |         |         |         |         | proceed |
|         |         |         |         |         |         | ings/pa |
|         |         |         |         |         |         | pers/ge |
|         |         |         |         |         |         | rmeval/ |
|         |         |         |         |         |         | GermEva |
|         |         |         |         |         |         | lShared |
|         |         |         |         |         |         | Task201 |
|         |         |         |         |         |         | 9Iggsa. |
|         |         |         |         |         |         | pdf>`__ |
+---------+---------+---------+---------+---------+---------+---------+
| OL19-C  | 👿      | tweets  | 1921    | 930     | binary  | G       |
|         | e       |         |         |         | (ex     | ermEval |
|         | xplicit |         |         |         | plicit, | 2018,   |
|         | vs. i   |         |         |         | im      | `📁 <h  |
|         | mplicit |         |         |         | plicit) | ttps:// |
|         | offense |         |         |         |         | project |
|         |         |         |         |         |         | s.fzai. |
|         |         |         |         |         |         | h-da.de |
|         |         |         |         |         |         | /iggsa/ |
|         |         |         |         |         |         | data-20 |
|         |         |         |         |         |         | 19/>`__ |
|         |         |         |         |         |         | `📖 <   |
|         |         |         |         |         |         | https:/ |
|         |         |         |         |         |         | /corpor |
|         |         |         |         |         |         | a.lingu |
|         |         |         |         |         |         | istik.u |
|         |         |         |         |         |         | ni-erla |
|         |         |         |         |         |         | ngen.de |
|         |         |         |         |         |         | /data/k |
|         |         |         |         |         |         | onvens/ |
|         |         |         |         |         |         | proceed |
|         |         |         |         |         |         | ings/pa |
|         |         |         |         |         |         | pers/ge |
|         |         |         |         |         |         | rmeval/ |
|         |         |         |         |         |         | GermEva |
|         |         |         |         |         |         | lShared |
|         |         |         |         |         |         | Task201 |
|         |         |         |         |         |         | 9Iggsa. |
|         |         |         |         |         |         | pdf>`__ |
+---------+---------+---------+---------+---------+---------+---------+
| OL18-A  | 👿      | tweets  | 5009    | 3398    | binary  | G       |
|         | of      |         |         |         | {0,1}   | ermEval |
|         | fensive |         |         |         |         | 2018,   |
|         | l       |         |         |         |         | `📁 <   |
|         | anguage |         |         |         |         | https:/ |
|         |         |         |         |         |         | /github |
|         |         |         |         |         |         | .com/ud |
|         |         |         |         |         |         | s-lsv/G |
|         |         |         |         |         |         | ermEval |
|         |         |         |         |         |         | -2018-D |
|         |         |         |         |         |         | ata>`__ |
+---------+---------+---------+---------+---------+---------+---------+
| OL18-B  | 👿      | tweets  | 5009    | 3398    | 4 catg. | G       |
|         | of      |         |         |         | (pro    | ermEval |
|         | fensive |         |         |         | fanity, | 2018,   |
|         | la      |         |         |         | insult, | `📁 <   |
|         | nguage, |         |         |         | abuse,  | https:/ |
|         | fine-   |         |         |         | oth.)   | /github |
|         | grained |         |         |         |         | .com/ud |
|         |         |         |         |         |         | s-lsv/G |
|         |         |         |         |         |         | ermEval |
|         |         |         |         |         |         | -2018-D |
|         |         |         |         |         |         | ata>`__ |
+---------+---------+---------+---------+---------+---------+---------+
| ABSD-1  | 🛤️      | ‘D      | 19432   | 2555    | binary  | G       |
|         | re      | eutsche |         |         |         | ermEval |
|         | levance | Bahn’   |         |         |         | 2017,   |
|         | classif | c       |         |         |         | `📁 <   |
|         | ication | ustomer |         |         |         | https:/ |
|         |         | fe      |         |         |         | /sites. |
|         |         | edback, |         |         |         | google. |
|         |         | ``lang: |         |         |         | com/vie |
|         |         | de-DE`` |         |         |         | w/germe |
|         |         |         |         |         |         | val2017 |
|         |         |         |         |         |         | -absa/d |
|         |         |         |         |         |         | ata>`__ |
+---------+---------+---------+---------+---------+---------+---------+
| ABSD-2  | 🛤️      | ‘D      | 19432   | 2555    | 3 catg. | G       |
|         | Se      | eutsche |         |         | (pos.,  | ermEval |
|         | ntiment | Bahn’   |         |         | neg.,   | 2017,   |
|         | a       | c       |         |         | n       | `📁 <   |
|         | nalysis | ustomer |         |         | eutral) | https:/ |
|         |         | fe      |         |         |         | /sites. |
|         |         | edback, |         |         |         | google. |
|         |         | ``lang: |         |         |         | com/vie |
|         |         | de-DE`` |         |         |         | w/germe |
|         |         |         |         |         |         | val2017 |
|         |         |         |         |         |         | -absa/d |
|         |         |         |         |         |         | ata>`__ |
+---------+---------+---------+---------+---------+---------+---------+
| ABSD-3  | 🛤️      | ‘D      | 19432   | 2555    | 20      | G       |
|         | aspect  | eutsche |         |         | catg.   | ermEval |
|         | cat     | Bahn’   |         |         |         | 2017,   |
|         | egories | c       |         |         |         | `📁 <   |
|         |         | ustomer |         |         |         | https:/ |
|         |         | fe      |         |         |         | /sites. |
|         |         | edback, |         |         |         | google. |
|         |         | ``lang: |         |         |         | com/vie |
|         |         | de-DE`` |         |         |         | w/germe |
|         |         |         |         |         |         | val2017 |
|         |         |         |         |         |         | -absa/d |
|         |         |         |         |         |         | ata>`__ |
+---------+---------+---------+---------+---------+---------+---------+
| MIO-S   | Se      | ‘Der    | 1799    | 1800    | 3 catg. | One     |
|         | ntiment | St      |         |         |         | Million |
|         | a       | andard’ |         |         |         | Posts   |
|         | nalysis | ne      |         |         |         | Corpus, |
|         |         | wspaper |         |         |         | `📁     |
|         |         | article |         |         |         |  <http  |
|         |         | web     |         |         |         | s://git |
|         |         | co      |         |         |         | hub.com |
|         |         | mments, |         |         |         | /OFAI/m |
|         |         | ``lang: |         |         |         | illion- |
|         |         | de-AT`` |         |         |         | post-co |
|         |         |         |         |         |         | rpus/re |
|         |         |         |         |         |         | leases/ |
|         |         |         |         |         |         | tag/v1. |
|         |         |         |         |         |         | 0.0>`__ |
+---------+---------+---------+---------+---------+---------+---------+
| MIO-O   | of      | ‘Der    | 1799    | 1800    | binary  | One     |
|         | f-topic | St      |         |         |         | Million |
|         | c       | andard’ |         |         |         | Posts   |
|         | omments | ne      |         |         |         | Corpus, |
|         |         | wspaper |         |         |         | `📁     |
|         |         | article |         |         |         |  <http  |
|         |         | web     |         |         |         | s://git |
|         |         | co      |         |         |         | hub.com |
|         |         | mments, |         |         |         | /OFAI/m |
|         |         | ``lang: |         |         |         | illion- |
|         |         | de-AT`` |         |         |         | post-co |
|         |         |         |         |         |         | rpus/re |
|         |         |         |         |         |         | leases/ |
|         |         |         |         |         |         | tag/v1. |
|         |         |         |         |         |         | 0.0>`__ |
+---------+---------+---------+---------+---------+---------+---------+
| MIO-I   | inappr  | ‘Der    | 1799    | 1800    | binary  | One     |
|         | opriate | St      |         |         |         | Million |
|         | c       | andard’ |         |         |         | Posts   |
|         | omments | ne      |         |         |         | Corpus, |
|         |         | wspaper |         |         |         | `📁     |
|         |         | article |         |         |         |  <http  |
|         |         | web     |         |         |         | s://git |
|         |         | co      |         |         |         | hub.com |
|         |         | mments, |         |         |         | /OFAI/m |
|         |         | ``lang: |         |         |         | illion- |
|         |         | de-AT`` |         |         |         | post-co |
|         |         |         |         |         |         | rpus/re |
|         |         |         |         |         |         | leases/ |
|         |         |         |         |         |         | tag/v1. |
|         |         |         |         |         |         | 0.0>`__ |
+---------+---------+---------+---------+---------+---------+---------+
| MIO-D   | discrim | ‘Der    | 1799    | 1800    | binary  | One     |
|         | inating | St      |         |         |         | Million |
|         | c       | andard’ |         |         |         | Posts   |
|         | omments | ne      |         |         |         | Corpus, |
|         |         | wspaper |         |         |         | `📁     |
|         |         | article |         |         |         |  <http  |
|         |         | web     |         |         |         | s://git |
|         |         | co      |         |         |         | hub.com |
|         |         | mments, |         |         |         | /OFAI/m |
|         |         | ``lang: |         |         |         | illion- |
|         |         | de-AT`` |         |         |         | post-co |
|         |         |         |         |         |         | rpus/re |
|         |         |         |         |         |         | leases/ |
|         |         |         |         |         |         | tag/v1. |
|         |         |         |         |         |         | 0.0>`__ |
+---------+---------+---------+---------+---------+---------+---------+
| MIO-F   | f       | ‘Der    | 3019    | 3019    | binary  | One     |
|         | eedback | St      |         |         |         | Million |
|         | c       | andard’ |         |         |         | Posts   |
|         | omments | ne      |         |         |         | Corpus, |
|         |         | wspaper |         |         |         | `📁     |
|         |         | article |         |         |         |  <http  |
|         |         | web     |         |         |         | s://git |
|         |         | co      |         |         |         | hub.com |
|         |         | mments, |         |         |         | /OFAI/m |
|         |         | ``lang: |         |         |         | illion- |
|         |         | de-AT`` |         |         |         | post-co |
|         |         |         |         |         |         | rpus/re |
|         |         |         |         |         |         | leases/ |
|         |         |         |         |         |         | tag/v1. |
|         |         |         |         |         |         | 0.0>`__ |
+---------+---------+---------+---------+---------+---------+---------+
| MIO-P   | p       | ‘Der    | 4668    | 4668    | binary  | One     |
|         | ersonal | St      |         |         |         | Million |
|         | story   | andard’ |         |         |         | Posts   |
|         | c       | ne      |         |         |         | Corpus, |
|         | omments | wspaper |         |         |         | `📁     |
|         |         | article |         |         |         |  <http  |
|         |         | web     |         |         |         | s://git |
|         |         | co      |         |         |         | hub.com |
|         |         | mments, |         |         |         | /OFAI/m |
|         |         | ``lang: |         |         |         | illion- |
|         |         | de-AT`` |         |         |         | post-co |
|         |         |         |         |         |         | rpus/re |
|         |         |         |         |         |         | leases/ |
|         |         |         |         |         |         | tag/v1. |
|         |         |         |         |         |         | 0.0>`__ |
+---------+---------+---------+---------+---------+---------+---------+
| MIO-A   | argume  | ‘Der    | 1799    | 1800    | binary  | One     |
|         | ntative | St      |         |         |         | Million |
|         | c       | andard’ |         |         |         | Posts   |
|         | omments | ne      |         |         |         | Corpus, |
|         |         | wspaper |         |         |         | `📁     |
|         |         | article |         |         |         |  <http  |
|         |         | web     |         |         |         | s://git |
|         |         | co      |         |         |         | hub.com |
|         |         | mments, |         |         |         | /OFAI/m |
|         |         | ``lang: |         |         |         | illion- |
|         |         | de-AT`` |         |         |         | post-co |
|         |         |         |         |         |         | rpus/re |
|         |         |         |         |         |         | leases/ |
|         |         |         |         |         |         | tag/v1. |
|         |         |         |         |         |         | 0.0>`__ |
+---------+---------+---------+---------+---------+---------+---------+
| SBCH-L  | Swiss   | ‘cha    | 748     | 748     | binary  | SB-CH   |
|         | German  | tmania’ |         |         |         | Corpus, |
|         | de      | app     |         |         |         | `📁 <   |
|         | tection | co      |         |         |         | https:/ |
|         |         | mments, |         |         |         | /github |
|         |         | ``lan   |         |         |         | .com/sp |
|         |         | g:gsw`` |         |         |         | inningb |
|         |         |         |         |         |         | ytes/SB |
|         |         |         |         |         |         | -CH>`__ |
+---------+---------+---------+---------+---------+---------+---------+
| SBCH-S  | Se      | ‘cha    | 394     | 394     | 3 catg. | SB-CH   |
|         | ntiment | tmania’ |         |         |         | Corpus, |
|         | a       | app     |         |         |         | `📁 <   |
|         | nalysis | co      |         |         |         | https:/ |
|         |         | mments, |         |         |         | /github |
|         |         | only    |         |         |         | .com/sp |
|         |         | c       |         |         |         | inningb |
|         |         | omments |         |         |         | ytes/SB |
|         |         | l       |         |         |         | -CH>`__ |
|         |         | abelled |         |         |         |         |
|         |         | as      |         |         |         |         |
|         |         | Swiss   |         |         |         |         |
|         |         | German  |         |         |         |         |
|         |         | are     |         |         |         |         |
|         |         | in      |         |         |         |         |
|         |         | cluded, |         |         |         |         |
|         |         | ``lan   |         |         |         |         |
|         |         | g:gsw`` |         |         |         |         |
+---------+---------+---------+---------+---------+---------+---------+
| ARCHI   | Swiss   | ``lan   | 18809   | 4743    | 4 catg. | Ar      |
|         | German  | g:gsw`` |         |         |         | chiMob, |
|         | Dialect |         |         |         |         | `📁     |
|         | Classif |         |         |         |         |  <https |
|         | ication |         |         |         |         | ://www. |
|         |         |         |         |         |         | spur.uz |
|         |         |         |         |         |         | h.ch/en |
|         |         |         |         |         |         | /depart |
|         |         |         |         |         |         | ments/r |
|         |         |         |         |         |         | esearch |
|         |         |         |         |         |         | /textgr |
|         |         |         |         |         |         | oup/Arc |
|         |         |         |         |         |         | hiMob.h |
|         |         |         |         |         |         | tml>`__ |
|         |         |         |         |         |         | `       |
|         |         |         |         |         |         | 📖 <htt |
|         |         |         |         |         |         | ps://ac |
|         |         |         |         |         |         | lanthol |
|         |         |         |         |         |         | ogy.org |
|         |         |         |         |         |         | /W19-14 |
|         |         |         |         |         |         | 01/>`__ |
+---------+---------+---------+---------+---------+---------+---------+
| LSDC    | Lower   | ``lan   | 74140   | 8602    | 14      | LSDC,   |
|         | Saxon   | g:nds`` |         |         | catg.   | `📁     |
|         | Dialect |         |         |         |         |  <https |
|         | Classif |         |         |         |         | ://gith |
|         | ication |         |         |         |         | ub.com/ |
|         |         |         |         |         |         | Helsink |
|         |         |         |         |         |         | i-NLP/L |
|         |         |         |         |         |         | SDC>`__ |
|         |         |         |         |         |         | `📖     |
|         |         |         |         |         |         |  <http  |
|         |         |         |         |         |         | s://www |
|         |         |         |         |         |         | .aclweb |
|         |         |         |         |         |         | .org/an |
|         |         |         |         |         |         | thology |
|         |         |         |         |         |         | /2020.v |
|         |         |         |         |         |         | ardial- |
|         |         |         |         |         |         | 1.3>`__ |
+---------+---------+---------+---------+---------+---------+---------+

Download datasets
-----------------

.. code:: sh

   bash download-datasets.sh

Usage example
-------------

.. code:: py

   from typing import List
   import sentence_embedding_evaluation_german as seeg
   import torch

   # (1) Instantiate your Embedding model
   emb_dim = 512
   vocab_sz = 128
   emb = torch.randn((vocab_sz, emb_dim), requires_grad=False)
   emb = torch.nn.Embedding.from_pretrained(emb)
   assert emb.weight.requires_grad == False

   # (2) Specify the preprocessing
   def preprocesser(batch: List[str], params: dict=None) -> List[List[float]]:
       """ Specify your embedding or pretrained encoder here
       Paramters:
       ----------
       params : dict
           The params dictionary
       batch : List[str]
           A list of sentence as string
       Returns:
       --------
       List[List[float]]
           A list of embedding vectors
       """
       features = []
       for sent in batch:
           try:
               ids = torch.tensor([ord(c) % 128 for c in sent])
           except:
               print(sent)
           h = emb(ids)
           features.append(h.mean(axis=0))
       features = torch.stack(features, dim=0)
       return features

   # (3) Training settings
   params = {
       'datafolder': '../datasets',
       'batch_size': 128, 
       'num_epochs': 20,
       # 'early_stopping': True,
       # 'split_ratio': 0.2,  # if early_stopping=True
       # 'patience': 5,  # if early_stopping=True
   }

   # (4) Specify downstream tasks
   downstream_tasks = ['FCLAIM', 'VMWE', 'OL19-C', 'ABSD-2', 'MIO-P', 'ARCHI', 'LSDC']

   # (5) Run experiments
   results = seeg.evaluate(downstream_tasks, preprocesser, **params)

Appendix
--------

Installation
~~~~~~~~~~~~

The ``sentence-embedding-evaluation-german`` `git
repo <http://github.com/ulf1/sentence-embedding-evaluation-german>`__ is
available as `PyPi
package <https://pypi.org/project/sentence-embedding-evaluation-german>`__

.. code:: sh

   pip install sentence-embedding-evaluation-german
   pip install git+ssh://git@github.com/ulf1/sentence-embedding-evaluation-german.git

Install a virtual environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: sh

   python3.7 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt --no-cache-dir
   pip install -r requirements-dev.txt --no-cache-dir
   pip install -r requirements-demo.txt --no-cache-dir

(If your git repo is stored in a folder with whitespaces, then don’t use
the subfolder ``.venv``. Use an absolute path without whitespaces.)

Python commands
~~~~~~~~~~~~~~~

-  Jupyter for the examples: ``jupyter lab``
-  Check syntax:
   ``flake8 --ignore=F401 --exclude=$(grep -v '^#' .gitignore | xargs | sed -e 's/ /,/g')``

Publish

.. code:: sh

   pandoc README.md --from markdown --to rst -s -o README.rst
   python setup.py sdist 
   twine upload -r pypi dist/*

Clean up
~~~~~~~~

.. code:: sh

   find . -type f -name "*.pyc" | xargs rm
   find . -type d -name "__pycache__" | xargs rm -r
   rm -r .pytest_cache
   rm -r .venv

Support
~~~~~~~

Please `open an
issue <https://github.com/ulf1/sentence-embedding-evaluation-german/issues/new>`__
for support.

Contributing
~~~~~~~~~~~~

Please contribute using `Github
Flow <https://guides.github.com/introduction/flow/>`__. Create a branch,
add commits, and `open a pull
request <https://github.com/ulf1/sentence-embedding-evaluation-german/compare/>`__.

.. |PyPI version| image:: https://badge.fury.io/py/sentence-embedding-evaluation-german.svg
   :target: https://badge.fury.io/py/sentence-embedding-evaluation-german
.. |Total alerts| image:: https://img.shields.io/lgtm/alerts/g/ulf1/sentence-embedding-evaluation-german.svg?logo=lgtm&logoWidth=18
   :target: https://lgtm.com/projects/g/ulf1/sentence-embedding-evaluation-german/alerts/
.. |Language grade: Python| image:: https://img.shields.io/lgtm/grade/python/g/ulf1/sentence-embedding-evaluation-german.svg?logo=lgtm&logoWidth=18
   :target: https://lgtm.com/projects/g/ulf1/sentence-embedding-evaluation-german/context:python
