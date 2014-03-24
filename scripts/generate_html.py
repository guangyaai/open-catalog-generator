#!/usr/bin/python
import json
import re
import sys
import time
import os
import shutil
import darpa_open_catalog as doc
from pprint import pprint

active_content_file = sys.argv[1]
data_dir = sys.argv[2]
build_dir = sys.argv[3]
darpa_links = sys.argv[4]
date = time.strftime("%Y-%m-%d", time.localtime())

print """
Active content file: %s
Data directory: %s
Build directory: %s
""" % (active_content_file, data_dir, build_dir)

print "Attempting to load %s" %  active_content_file
active_content = json.load(open(active_content_file))

splash_page = doc.catalog_page_header()
splash_page += doc.logo("")
splash_page += doc.catalog_splash_content()
splash_page += doc.splash_table_header()

for program in active_content:
  program_name = program['Program Name']
  program_page_filename = program_name + ".html"
  program_page = doc.catalog_page_header()
  program_image_file = ""
  software_columns = []
  if program['Program File'] == "":
    print "ERROR: %s has no program details json file, can't continue.  Please fix this and restart the build." % program_name
    sys.exit(1)
  else:
    print "Attempting to load %s" %  program['Program File']
    program_details = json.load(open(data_dir + program['Program File']))
 
    program_page += doc.logo("<a href=\"http://www.darpa.mil/Our_Work/I2O/\"' style=\"color: #EBAF00;\"class='programlink'>Information Innovation Office (I2O)</a>")
    if re.search('^http',program_details['Link']):
      program_page += "\n  <h2><a href='" + program_details['Link'] + "' class='programlink'>" + program_details['Long Name'] + "</a></h2>\n"
    else:
      program_page += "<h2>%s</h2>" % program_details['Long Name']
    
    #program_page += "<h3><a href=\"http://www.darpa.mil/Our_Work/I2O/\"' class='programlink'>Information Innovation Office</a></h3>"
    program_page += "<div class='left-paragraph'><p>%s<p>" % program_details['Description']

    program_page += "<p>Program Manager: %s<p>" % program_details['Program Manager']
    program_page += "<p>Contact: <a href='mailto:%s'>%s</a><p>" % (program_details['Program Manager Email'], program_details['Program Manager Email'])
    program_page += "<p>The content below has been generated by organizations that are partially funded by DARPA; the views and conclusions contained therein are those of the authors and should not be interpreted as necessarily representing the official policies or endorsements, either expressed or implied, of DARPA or the U.S. Government.</p>"

    if program['Software File'] != "":
      program_page += "<ul><li>The Software Table lists performers with one row per piece of software. Each piece of software has licensing information, a link to an external project page or contact information, and where possible a link to the code repository for the project.</li></ul>"
    if program['Pubs File'] != "":
      program_page += "<ul><li>The Publications Table contains author(s), title, and links to peer-reviewed articles related to specific DARPA programs.</li></ul>"
    program_page += "<p>Report a problem: <a href=\"mailto:opencatalog@darpa.mil\">opencatalog@darpa.mil</a></p>"
    program_page += "<p>Last updated: %s</p></div>" % date
    if 'Image' in program_details.keys():
      if program_details['Image'] != "":
        program_page += "\n<div class='right-image'><img src=\"%s\"/></div>" % program_details['Image']
      program_image_file = program_details['Image']
    
    banner = ""
    program_link = "<a href='%s'>%s</a>" % (program_page_filename, program_details['DARPA Program Name'])
    if program['Banner'].upper() == "NEW":
      banner = "<div class='wrapper'><a href='%s'>%s</a><div class='ribbon-wrapper'><div class='ribbon-standard ribbon-red'>%s</div></div></div>"  % (program_page_filename, program_details['DARPA Program Name'], program['Banner'].upper())
    elif program['Banner'].upper() == "COMING SOON":
      banner = "<div class='wrapper'>%s<div class='ribbon-wrapper'><div class='ribbon-standard ribbon-blue'>%s</div></div></div>"  % (program_details['DARPA Program Name'], program['Banner'].upper())
    elif program['Banner'].upper() == "UPDATED":
      banner = "<div class='wrapper'><a href='%s'>%s</a><div class='ribbon-wrapper'><div class='ribbon-standard ribbon-green'>%s</div></div></div>"  % (program_page_filename, program_details['DARPA Program Name'], program['Banner'].upper())
    else:
     banner = "<a href='%s'>%s</a>" % (program_page_filename, program_details['DARPA Program Name'])
    splash_page += "<TR>\n <TD width=130> %s</TD>\n <TD>%s</TD>\n</TR>" % (banner, program_details['Description']) 
    software_columns = program_details['Display Software Columns']

  # This creates a hashed array (dictionary) of teams that have publications. We use this to cross link to them from the software table.
  pubs_exist = {}
  if program['Pubs File'] != "" and program['Software File'] != "":
      print "Attempting to load %s" %  program['Pubs File']
      pubs_file = open(data_dir + program['Pubs File'])
      pubs = json.load(pubs_file)
      pubs_file.close()
      #print "Attempting to load %s" %  program['Software File']
      #softwares = json.load(open(data_dir + program['Software File'])) 
      for pub in pubs:
        for team in pub['Program Teams']:
          pubs_exist[team] = 1


  #starts the tabs div for the Software and Publications tables
  search_tab = ""
  search_footer = ""
  program_page += "<div id='tabs' class='table-tabs'><ul>"
  if program['Software File'] != "":
    program_page += "<li><a href='#tabs0'>Software</a></li>"
    search_tab += "<div id='allSearch'><div id='tabs2'>"
    search_tab += "<div id='softwareSearch'><input class='search' placeholder='Search' id='search2' onkeyup='allSearch(this)'/>"
    search_tab += "<button class='clear_button' id='clear2'>Clear</button><div id='sftwrTable'><h2>Software</h2></div></div>"
    search_footer += "</div></div>"
  if program['Pubs File'] != "":
    program_page += "<li><a href='#tabs1'>Publications</a></li>"
    search_tab += "<div id='publicationsSearch'><div id='pubTable'><h2>Publications</h2></div></div>"
    program_page += "<li><a href='#tabs2'>Search</a></li>"
  program_page += "</ul>"
  
  if search_tab != "":
    search_tab += search_footer
  
  
  ###### SOFTWARE
  # ["Team","Software","Category","Code","Stats","Description","License"]
  if program['Software File'] != "":
    program_page += "<div id='software'><div id='tabs0'>"
    program_page += "<input class='search' placeholder='Search' id='search0'/>"
    program_page += "<button class='clear_button' id='clear0'>Clear</button>"
    print "Attempting to load %s" %  program['Software File']
    softwares = json.load(open(data_dir + program['Software File']))   
    program_page += doc.software_table_header(software_columns)
    for software in softwares:
      for column in software_columns:
        # Team
        if column == "Team":
          program_page += "<TR>\n  <TD class='%s'>" % column.lower()
          for team in software['Program Teams']:
            if team in pubs_exist:
              team += " <a href='#" + team + "' onclick='pubSearch(this)'>(publications)</a>"
            program_page += team + ", "
          program_page = program_page[:-2]
          program_page += "</TD>\n "
        # Software
        if column == "Software":
          # Debug
          #print "      " + software['Software']
          elink = ""
          if 'External Link' in software.keys():
            elink = software['External Link']
          if re.search('^http',elink) and elink != "":
            if darpa_links == "darpalinks":
              program_page += "  <TD class='%s'><a href='http://www.darpa.mil/External_Link.aspx?url=" + elink + "'>" + software['Software'] + "</a></TD>\n" % column.lower()
            else:
              program_page += "  <TD class=" + column.lower() + "><a href='" + elink + "'>" + software['Software'] + "</a></TD>\n"
          else:
            program_page += "  <TD class=" + column.lower() + ">" + software['Software'] + "</TD>\n"
        # Category
        if column == "Category":
          categories = ""
          if 'Categories' in software.keys():
            for category in software['Categories']:
              categories += category + ", "
            categories = categories[:-2]
          program_page += "  <TD class=" + column.lower() + ">" + categories + "</TD>\n"
        # Instructional Material
        if column == "Instructional Material":
          instructional_material = ""
          if 'Instructional Material' in software.keys():
            instructional_material = software['Instructional Material']
          if re.search('^http',instructional_material):
            if darpa_links == "darpalinks":
              program_page += "  <TD class='%s'><a href='http://www.darpa.mil/External_Link.aspx?url=" + instructional_material + "'> Documentation or Tutorial </a></TD>\n" % column.lower()
            else:
              program_page += "  <TD class=" + column.lower() + "><a href='" + instructional_material + "'> Documentation or Tutorial </a></TD>\n"
          else:
            program_page += "  <TD class=" + column.lower() + ">" + instructional_material + "</TD>\n"
        # Code
        if column == "Code":
          clink = ""
          if 'Public Code Repo' in software.keys():
            if program_details['DARPA Program Name'] == "DEFT":
			  clink = "<span class='code-mail' onclick='softwareRequest(\"" + program_details['DARPA Program Name'] + "\", \"" + software['Software'] + "\", \"" + doc.get_current_user() + "\");'>" + software['Public Code Repo'] + "</span>"
            else:
              clink = software['Public Code Repo']
          program_page += "  <TD class=" + column.lower() + "> " + clink + " </TD>\n"
        # Stats
        if column == "Stats":
          if 'Stats' in software.keys():
            if software['Stats'] != "":
              slink = software['Stats']
              program_page += "  <TD class=" + column.lower() + "> <a href='stats/" + slink + "/activity.html'>stats</a> </TD>\n"
            else: 
              program_page += "  <TD class=" + column.lower() + "></TD>\n"
          else:
            program_page += "  <TD class=" + column.lower() + "></TD>\n"
    
        # Description
        if column == "Description":
          program_page += " <TD class=" + column.lower() + "> " + software['Description'] + " </TD>\n"
        # License
        if column == "License":
          program_page += " <TD class=" + column.lower() + "> " + software['License'] + " </TD>\n </TR>\n"
    program_page += doc.software_table_footer()
    program_page += "</div></div>"
	

####### Publications
  if program['Pubs File'] != "":
    program_page += "<div id='publications'><div id='tabs1'>"
    program_page += "<input class='search' placeholder='Search' id='search1'/>"
    program_page += "<button class='clear_button' id='clear1'>Clear</button>"
    print "Attempting to load %s" %  program['Pubs File']
    pubs = json.load(open(data_dir + program['Pubs File']))
    program_page += doc.pubs_table_header()
    for pub in pubs:
      program_page += "<TR>\n  <TD class='team'>" 
      for team in pub['Program Teams']:
        program_page += team + "<a name='" + team + "'>, "
      program_page = program_page[:-2]
      program_page += "</TD>\n  <TD class='title'>" + pub['Title'] + "</TD>\n"
      link = pub['Link']
      if re.search('^http',link) or re.search('^ftp',link):
        if darpa_links == "darpalinks":
          program_page += "  <TD class='link'><a href='http://www.darpa.mil/External_Link.aspx?url=" + link + "'>" + link + "</a></TD>\n"
        else:
          program_page += "  <TD class='link'><a href='" + link + "'>" + link + "</a></TD>\n"
      else:
        program_page += "  <TD class='link'>" + link + "</TD>\n"
      program_page += "</TR>\n"
    program_page += doc.pubs_table_footer() + "</div></div>"
    program_page += search_tab	
  program_page += "</div><br>\n"
  program_page += doc.catalog_page_footer()
  
  if program['Banner'].upper() != "COMING SOON":
    print "Writing to %s" % build_dir + '/' + program_page_filename
    program_outfile = open(build_dir + '/' + program_page_filename, 'w')
    program_outfile.write(program_page)
    if program_image_file != "":
      shutil.copy(data_dir + program_image_file, build_dir)

splash_page += doc.splash_table_footer()
splash_page += doc.catalog_page_footer()

splash_page_file = build_dir + '/index.html'
print "Writing to %s" % splash_page_file
splash_outfile = open(splash_page_file, 'w')
splash_outfile.write(splash_page)





























































