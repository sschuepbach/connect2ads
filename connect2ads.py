from bs4 import BeautifulSoup
from calendar import monthrange
import urllib.request
import urllib.parse
import subprocess
import re
import os
import argparse


def geturlsads(searchstring="",
               querytype="pattern",
               titleweight="false",
               titlestring="",
               fromdate="01.01.1848",
               todate="31.12.2014",
               volno="",
               bookletno="",
               doctype=list(),
               category="",
               council="",
               fileno="",
               author="",
               refno="",
               lang=""):
    """
    Die Funktion geturlsads sucht in den Amtsdruckschriften (http://www.amtsdruckschriften.bar.admin.ch
    nach Dokumenten, die den gesuchten Kriterien entsprechen. Folgende Suchparameter können dabei gesetzt werden:
    - searchstring: Suchterm
    - querytype: exakte oder unscharfe Suche nach Term
    - titleweight: Resultate mit Suchterm im Titel werden mehr gewichtet.
    - titlestring: Suchterm im Titel
    - fromdate: Startdatum.
    - todate: Enddatum.
    - volno: Bandnummer
    - bookletno: Heft-/Dokumentennummer
    - category: Dokumententyp.
    - council: Behandelnder Rat
    - fileno: Geschäftsnummer
    - author: Autor
    - refno: Referenznummer
    - lang: Sprache
    Die Funktion gibt eine Liste zurück, in der für jedes Dokument in einem Diktionär
    folgende Daten (sofern vorhanden) gespeichert werden:
    - id: ID
    - url: URL des PDF
    - typ: Oberkategorie (bspw. Bundesblatt)
    - jahr: Jahr
    - band: Band
    - seitevon: Erste Seite (falls Teil von grösserem Band)
    - seitebis: Letzte Seite (falls Teil von grösserem Band)
    - kategorie: Unterkategorie (für jede Oberkategorie verschieden)
    - rat: Rat (bei Unterlagen des Parlaments)
    - autor: Autor (bei Publikationen)

    :param searchstring:
    Suchterm
    String wird enkodiert

    :param querytype:
    Exakte oder unscharfe Suche nach Term
    Mögliche Werte: {boolean, pattern}

    :param titleweight:
    Resultate mit Suchterm im Titel werden mehr gewichtet.
    Mögliche Werte: {false, on}

    :param titlestring:
    Suchterm im Titel

    :param fromdate:
    Datumsformat: In der Form "dd.mm.yyyy"

    :param todate:
    Datumsformat: In der Form "dd.mm.yyyy"

    :param volno:
    Bandnummer

    :param bookletno:
    Heft-/Dokumentennummer

    :param category:
    Dokumententyp
    Mögliche Werte:
    "AB": Amtliches Bulletin
        "AB_ANF": Anfrage
        "AB_EMPF": Empfehlung
        "AB_FRAH": Fragestunde
        "AB_INH": Inhaltsverzeichnisse/Rednerlisten
        "AB_IP": Interpellation
        "AB_JINH": Jahres-Inhaltsverzeichnisse/Jahres-Rednerlisten
        "AB_MO": Motion
        "AB_PIN": Parlamentarische Initiative
        "AB_PET": Petition
        "AB_POST": Postulat
        "AB_SR": Sachregister
        "AB_SIN": Standesinitiative
        "AB_VER": Verschiedenes
        "AB_VORBR": Vorlage des Bundesrates
        "AB_VORP": Vorlage des Parlaments
    "BBL": Bundesblatt
        "BBL_ABK": Abkommen
        "BBL_AZ": Anzeigen
        "BBL_VdBV": Aus den Verhandlungen der Bundesversammlung
        "BBL_VdBG": Aus den Verhandlungen des Bundesgerichts
        "BBL_VdB": Aus den Verhandlungen des Bundesrats
        "BBL_BM": Bekanntmachungen
        "BBL_BR": Berichte
        "BBL_BO": Botschaft
        "BBL_BB: Bundesbeschluss
        "BBL_BG": Bundesgesetz
        "BBL_BRB": Bundesratsbeschluss
        "BBL_GS": Gesetz
        "BBL_IDX": Index
        "BBL_JB": Jahresbericht
        "BBL_KS": Kreisschreiben
        "BBL_PI": Parlamentarische Initiative
        "BBL_VRD": Verordnungen/Regelungen/Dekrete
        "BBL_DEF": Übrige
    "BRP": Bundesratsprotokolle
        "BRP_PROT_BR": Protokolle
        "BRP_REG_VGB": Register Verhandlungen Gotthardbahn
        "BRP_REG_SNO": Sach-, Namen- und Ortsregister
        "DEF": Übrige (!)
    "DDS": Diplomatische Dokumente der Schweiz
        "DDS_aae": Abessinien/Äthiopien
        "DDS_all": Allierte
        "DDS_arg": Argentinien
        "DDS_asyl": Asylpolitik
        "DDS_ausl": Ausländerpolitik
        "DDS_auspol": Aussenpolitik (allgemein)
        "DDS_ausw": Auswanderung/Auslandschweizer
        "DDS_bel": Belgien
        "DDS_bol": Bolivien
        "DDS_bras": Brasilien
        "DDS_bul": Bulgarien
        "DDS_chile": Chile
        "DDS_china": China
        "DDS_cr": Costa Rica
        "DDS_de": Deutschland
        "DDS_dom": Dominikanische Republik
        "DDS_dan": Dänemark
        "DDS_ecu": Ecuador
        "DDS_chb": Eidgenössische Behörden
        "DDS_finanz": Finanzplatz
        "DDS_fin": Finnland
        "DDS_fran": Frankreich
        "DDS_frem": Fremde Interessen
        "DDS_fried": Friedenspolitik/Sicherheitspolitik
        "DDS_gekonv": Genfer Konvention
        "DDS_griech": Griechenland
        "DDS_gb": Grossbritannien
        "DDS_guat": Guatemala
        "DDS_gd": Gute Dienste
        "DDS_haag": Haager Konferenzen und Konventionen
        "DDS_halt": Haltungen gegenüber Verfolgung
        "DDS_hum": Humanitäre Hilfe
        "DDS_ikrk": IKRK
        "DDS_inpol": Innenpolitische Angelegenheiten
        "DDS_ntern": Internierte
        "DDS_it": Italien
        "DDS_jap": Japan
        "DDS_jug": Jugoslawien
        "DDS_kol" Kolumbien
        "DDS_kong": Kongo
        "DDS_kor": Korea
        "DDS_krext": Kriegsmaterialexport und -transit
        "DDS_krim": Kriegsmaterialimport
        "DDS_li" Liechtenstein
        "DDS_mex": Mexiko
        "DDS_mil": Militärpolitik
        "DDS_mb": Multilaterale Beziehungen
        "DDS_np": Neutralitätspolitik
        "DDS_nl": Niederlande
        "DDS_nor": Norwegen
        "DDS_osm": Osmanisches Reich/Türkei
        "DDS_par": Paraguay
        "DDS_per": Persien/Iran
        "DDS_phi": Philippinen
        "DDS_pol": Polen
        "DDS_port": Portugal
        "DDS_pm": Presse und Medien
        "DDS_rb: Rechtsextreme Bewegungen
        "DDS_rf": Religiöse Bewegungen
        "DDS_revb": Revolutionäre Bewegungen
        "DDS_rum": Rumänien
        "DDS_rus": Russland/UdSSR
        "DDS_sw": Schweden
        "DDS_sia": Siam/Thailand
        "DDS_spa": Spanien
        "DDS_tv": Transit und Verkehr
        "DDS_tsch": Tschechoslowakei
        "DDS_uno": UNO
        "DDS_ung": Ungarn
        "DDS_uru": Uruguay
        "DDS_vat": Vatikan
        "DDS_usa": Vereinigte Staaten von Amerika
        "DDS_vb": Völkerbund
        "DDS_wirt": Wirtschaftspolitik
        "DDS_wp": Währungspolitik
        "DDS_zent": Zentralmächte/Achsenmächte
        "DDS_agy": Ägypten
        "DDS_oest": Österreich(-Ungarn)
        "DDS_DEF": Übrige
    "GB": Geschäftsberichte des Bundesrates
        "GB_BER": Berichte
        "GB_INH": Inhaltsverzeichnis
        "GB_MP": Motionen und Postulate
    "RV": Repertorium der Verhandlungen
    "SK": Staatskalender
        "SK_160ANV": Alphabetisches Namensverzeichnis
        "SK_048VAS": Ausländische Vertretungen in der Schweiz
        "SK_030BK": Bundeskanzlei
        "SK_020BRG": Bundesversammlung, Ràte, Gerichte
        "SK_045DA": Departement des Auswärtigen
        "SK_051DIB": Departement des Innern und des Bauwesens
        "SK_072VBS": Eidgenössisches Departement Verteidigung, Bevölkerungsschutz und Sport
        "SK_052EDI": Eidgenössisches Departement des Innern
        "SK_049EDA": Eidgenössisches Departement für auswärtige Angelegenheiten
        "SK_110EFA": Eidgenössisches Ernährungsamt
        "SK_082EFZ": Eidgenössisches Finanz und Zolldepartement
        "SK_083EFD": Eidgenössisches Finanzdepartement
        "SK_060EJPD": Eidgenössisches Justiz- und Polizeidepartement
        "SK_071EMP": Eidgenössisches Militärdepartement
        "SK_106VED": Eidgenössisches Verkehrs- und Energiewirtschaftsdepartement
        "SK_095EVD": Eidgenössisches Volkswirtschaftsdepartement
        "SK_104EHD": Eisenbahn- und Handelsdepartement
        "SK_081ETAT": Etats
        "SK_094HILD": Handels-, Industrie- und Landwirtschaftsdepartement
        "SK_093HLD": Handels- und Landwirtschaftsdepartement
        "SK_091HZ": Handels- und Zolldepartement
        "SK_010IOA": Index, Organigramm, Abkürzungsverzeichnis, Titel, Umschlag
        "SK_092ILD": Industrie- und Landwirtschaftsdepartement
        "SK_140IB": Internationale Bureaux
        "SK_500NTRG": Nachträge und Beilagen
        "SK_040PD": Politisches Departement
        "SK_130PS": Polytechnische Schule
        "SK_101PBD": Post- und Baudepartement
        "SK_105PED": Post- und Eisenbahndepartement
        "SK_103PTD": Post- und Telegraphendepartement
        "SK_102POST": Postdepartement
        "SK_047SVA": Schweizer Vertretungen im Ausland
        "SK_150SI": Sonstige Institutionen
        "SK_120SV": Spezielle Verwaltungen
    "SQ": Studien und Quellen
        "SQ_AUF": Aufsätze
        "SQ_EIN": Einleitung
        "SQ_IND": Index
        "SQ_INH": Inhalt
        "SQ_VW": Vorwort
        "SQ_ZF": Zusammenfassung
        "SQ_DEF": Übrige
    "SV": Staatsrechnung und Voranschlag
        "SV_BOT": Botschaft
        "SV_BO_TAB": Botschaft und Tabellen
        "SV_BB": Bundesbeschluss
        "SV_FR": Finanzrechnung
        "SV_FV": Finanzvorschlag
        "SV_SR": Staatsrechnung
        "SV_V": Voranschlag
        "SV_DEF": Übrige
    "SWB": Protokolle der Bundesversammlung
        "Index_SWB": Inhaltsverzeichnis
        "NR_SWB": Nationalrat
        "SR_SWB": Ständerat
        "Titel_SWB": Titelblatt
        "BV_SWB": Vereinigte Bundesversammlung
    "UEV": Übersicht über die Verhandlungen
        "Inh_UEV": Inhaltsverzeichnis
        "Über_UEV": Übersicht über die Verhandlungen

    :param council:
    Behandelnder Rat
    Mögliche Werte:
    "Nationalrat"
    "Ständerat"
    "Vereinigte+Bundesversammlung"

    :param fileno:
    Geschäftsnummer

    :param author:
    AutorIn

    :param refno:
    Referenznummer

    :param lang:
    Sprache
    Mögliche Werte:
    "*D*": Deutsch
    "*F*": Französisch
    "*I*": Italienisch

    :return:
    """
    urlstem = "http://www.amtsdruckschriften.bar.admin.ch/"
    dateslist = list()
    fromdate = fromdate.rsplit(".")
    todate = todate.rsplit(".")
    # Prüft, ob sich die Zeitspanne innerhalb eines Monats befindet. Falls ja, wird Such-Url direkt erstellt
    if fromdate[1] == todate[1] and fromdate[2] == todate[2]:
        dateslist.append(".".join(fromdate))
        dateslist.append(".".join(todate))
    # Falls nein, wird die Zeitspanne in einzelne Monate aufgeteilt,
    # um die obere Grenze bei der Resultatausgabe nicht zu überschreiten.
    else:
        dateslist.append(".".join(fromdate))
        days = str(monthrange(int(fromdate[2]), int(fromdate[1]))[1])
        dateslist.append(days + "." + ".".join(fromdate[1:]))
        y = 0
        month = int(fromdate[1])
        year = int(fromdate[2])
        while y < ((int(todate[2]) - int(fromdate[2])) * 12 +
                   int(todate[1]) - int(fromdate[1]) - 1):
            month += 1
            if month > 12:
                month = 1
                year += 1
            dateslist.append("01." + str(month).zfill(2) + "." + str(year))
            days = str(monthrange(year, month)[1])
            dateslist.append(days + "." + str(month).zfill(2) + "."
                             + str(year))
            y += 1
        dateslist.append("01." + ".".join(todate[1:]))
        dateslist.append(".".join(todate))
    url = list()
    for i in range(0, len(dateslist)-1, 2):
        doctypes = "&selectedDruckschrifttypen=" + "&selectedDruckschrifttypen=".join(doctype)
        url.append(urlstem +
                   "export.do?context=results&searchMode=advanced" +
                   "&queryString=" + urllib.parse.quote_plus(searchstring) +
                   "&queryType=" + querytype +  # boolean (=exakt) oder pattern (=unscharf)
                   "&titleWeight=" + titleweight +
                   "&title=" + urllib.parse.quote_plus(titlestring) +
                   doctypes +
                   "&daterange_from=" + dateslist[i] +
                   "&daterange_to=" + dateslist[i+1] +
                   "&fields[0].name=b_band_nr&fields[0].value=" + volno +
                   "&fields[1].name=a_heft_nr&fields[1].value=" + bookletno +
                   "&fields[2].name=t_textkategorie_abk&fields[2].value=" + category +
                   "&fields[3].name=a_anlass_ort_de&fields[3].value=" + council +
                   "&fields[4].name=t_geschaefts_nr&fields[4].value=" + fileno +
                   "&fields[5].name=t_autor&fields[5].value=" + urllib.parse.quote_plus(author) +
                   "&fields[6].name=t_texteinheit&fields[6]=" + refno +
                   "&fields[7].name=t_sprache&fields[7].value=" + "*" + lang + "*" +
                   "#resultlist")
    docsmeta = list()
    for i in url:
        opener = urllib.request.build_opener()
        opener.addheaders = [('Accept-Language', 'de-CH'),
                             ('Cookie', 'ADSGUI_Prefs="result.fields.selected=[a_druckschrifttyp_de%a_jahr%b_band_nr%t_seite_von%t_seite_bis%a_publikations_date%a_heft_nr%t_textkategorie_de%a_anlass_ort_kurz_de%t_geschaefts_nr%t_autor%t_texteinheit_id%t_sprache%false]:detail.docMarkupStyle=color:result.docsPerPage=50:detail.bestHitAutoJump=false:detail.documentFontSize=small:result.sortBy=relevance:result.maxDocs=100:search.advanced.titleWeight=on:result.resultsFontSize=x-small:result.sortOrder=asc"')]
        remotefile = opener.open(i)
        soup = BeautifulSoup(remotefile)("tr", class_="docsRow")
        redsoup = [tr for tr in soup if
                   len(BeautifulSoup(str(tr))("td")) == 17]
        for elem in redsoup:
            docdict = dict()
            docdict["id"] = (BeautifulSoup(str(elem))("td")[12]).get_text()
            docdict["url"] = urlstem + "/viewOrigDoc.do?id=" + docdict["id"] + "&action=download"
            docdict["titel"] = (BeautifulSoup(str(elem))("td")[0]).get_text()
            docdict["doktyp"] = (BeautifulSoup(str(elem))("td")[1]).get_text()
            docdict["jahr"] = (BeautifulSoup(str(elem))("td")[2]).get_text()
            docdict["band"] = (BeautifulSoup(str(elem))("td")[3]).get_text()
            docdict["seitevon"] = (BeautifulSoup(str(elem))("td")[4]).get_text()
            docdict["seitebis"] = (BeautifulSoup(str(elem))("td")[5]).get_text()
            docdict["zeitraum"] = (BeautifulSoup(str(elem))("td")[6]).get_text()
            docdict["heft"] = (BeautifulSoup(str(elem))("td")[7]).get_text()
            docdict["kategorie"] = (BeautifulSoup(str(elem))("td")[8]).get_text()
            docdict["rat"] = (BeautifulSoup(str(elem))("td")[9]).get_text()
            docdict["geschaeftsnr"] = (BeautifulSoup(str(elem))("td")[10]).get_text()
            docdict["autor"] = (BeautifulSoup(str(elem))("td")[11]).get_text()
            docdict["sprache"] = (BeautifulSoup(str(elem))("td")[13]).get_text()
            for element in docdict:
                if docdict[element] == "":
                    docdict[element] = None
            docsmeta.append(docdict)
    return docsmeta



def mdpdf(dokid, path):
    ofile = dokid + ".txt"
    # Anzahl Seiten werden aus den Metadaten des PDF ausgelesen
    pdfinfo = subprocess.check_output(["pdfinfo", path])
    lastpage = re.search("\nPages: *([0-9]{1,4})\n", pdfinfo.decode()).group(1)
    # Text der letzten Seite des PDF wird extrahiert
    subprocess.call(["pdftotext", "-q", "-f", lastpage, path, ofile])
    # Text wird zeilenweise aus Textdatei eingelesen
    rawmetadata = open(ofile, "r").read().split("\n")
    # Textdatei wird gelöscht
    os.remove(ofile)
    metadata = dict()
    # Seitenanzahl wird dem dict hinzugefügt
    metadata['seiten'] = lastpage
    # Das Dictionary enthält als Schlüssel die möglichen Metadaten, als Werte die Schlüssel für die Datenbankfelder
    mdentries = {"In": "inwerk", "Datum": "datum", "Teilbestand BAR": "teilbestand",
                 "Ablieferung BAR": "ablieferung", "Session": "session", "Sitzung": "sitzung",
                 "Signatur": "signatur", "Dokumentennr.": "doknr"}
    # Das Dictionary metadata enthält als Startwert für jedes mögliche Metadatum ein Leerwert
    for key in mdentries:
        metadata[mdentries[key]] = None
    # Wenn ein gesuchtes Metadatum in der zu untersuchenden Zeile in rawmetadata vorkommt, wird der Schlüsselwert,
    # der sich jeweils zwei Zeilen unterhalb des "Schlüssels" befindet, in metadata gespeichert. Die erste zu
    # untersuchende Zeile ist 8, da sich oberhalb jeweils keine relevanten Daten befinden
    index = 7
    for line in rawmetadata[7:]:
        if line in mdentries:
            if metadata[mdentries[line]] == "":
                metadata[mdentries[line]] = rawmetadata[index + 2]
        index += 1
    return metadata


if '__name__' == '__main__':
    parser = argparse.ArgumentParser(description="Extracts documents and metadata from Amtsdruckschriften")
    parser.add_argument('--searchstring', metavar='<str>', dest='searchstring', type=str, default='',
                        help='Search term(s)')
    parser.add_argument('--querytype', metavar='<str>', dest='querytype', type=str, choices=['boolean', 'pattern'],
                        default='boolean', help='Exact (boolean) or fuzzy (pattern) search. Defaults to boolean')
    parser.add_argument('--titleweight', metavar='<str>', dest='titleweight', type=str,
                        choices=['false', 'on'], default='false',
                        help='Terms in title are weighted more. Defaults to false')
    parser.add_argument('--titlestring', metavar='<str>', dest='titlestring', type=str, default='',
                        help='Search term(s) in title')
    # TODO: Right format should be checked
    parser.add_argument('--fromdate', metavar='<dd.mm.yyyy>', dest='fromdate', type=str, required=True,
                        help='Start date in form dd.mm.yyy')
    # TODO: Right format should be checked
    parser.add_argument('--todate', metavar='<dd.mm.yyyy>', dest='todate', type=str, required=True,
                        help='End date in form dd.mm.yyy')
    # TODO: Reformat as string
    parser.add_argument('--volno', metavar='<int>', dest='volno')
    # TODO: Reformat as string
    parser.add_argument('--bookletno', metavar='<int>')
    parser.add_argument('--doctype')
    parser.add_argument('--category')
    parser.add_argument('--council')
    parser.add_argument('--author')
    parser.add_argument('--refno')
    parser.add_argument('--lang')