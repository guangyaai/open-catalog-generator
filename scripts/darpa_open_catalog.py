#!/usr/bin/python
import time
import getpass
import re
import datetime
import change_timeline as timeline

def html_head():
  return """
  <!DOCTYPE html>
  <html lang='en'>
  <head>
  <meta charset="utf-8">
  <title>DARPA - Open Catalog</title>
  <link rel='stylesheet' href='css/style_v2.css' type='text/css'/>
  <link rel='stylesheet' href='css/banner_style.css' type='text/css'/>
  <link rel='stylesheet' href='css/flick/jquery-ui-1.10.4.custom.css' type='text/css'/>
  <link rel='stylesheet' href='css/list_style.css' type='text/css'/>
  <link rel='stylesheet' href='css/header_footer.css' type='text/css'/>
  <link rel='stylesheet' href="css/nv.d3.css" rel="stylesheet" type="text/css">  
  <script language="javascript" type='text/javascript' src="list.min.js"></script>
  <script language="javascript" type='text/javascript' src="d3.v3.js"></script>
  <script language="javascript" type='text/javascript' src="nv.d3.js"></script>
  <script language="javascript" type='text/javascript' src="tooltip.js"></script>
  <script language="javascript" type='text/javascript' src="nv.utils.js"></script>
  <script language="javascript" type='text/javascript' src="utils.js"></script>
  <script language="javascript" type='text/javascript' src="legend.js"></script>
  <script language="javascript" type='text/javascript' src="axis.js"></script>
  <script language="javascript" type='text/javascript' src="distribution.js"></script>
  <script language="javascript" type="text/javascript" src="jquery-1.11.1.min.js"></script>
  <script language="javascript" type='text/javascript' src="jquery-ui.js"></script>
  <script language="javascript" type='text/javascript' src='jquery.tablesorter.min.js'></script>
  </head>
  <body>
"""

def catalog_page_header(office_link):
  header = "<header class='darpa-header'><div class='darpa-header-images'><a href='http://www.darpa.mil/'><img class='darpa-logo' src='darpa-transparent-v2.png'></a><a href='index.html' class='programlink'><img src='Open-Catalog-Single-Big.png'></a></div>"
  if (office_link != ""):
    header += "<div class='darpa-header-text no-space'><span><font color='white'> / </font>%s</span></div></header>" % office_link
  header += "</header>"
  return header

def get_current_user():
  return getpass.getuser()
    
def catalog_splash_content():
  date = time.strftime("%Y-%m-%d", time.localtime())
  splash = """
<div width='98%'><p>Welcome to the DARPA Open Catalog, which contains a curated list of DARPA-sponsored software and peer-reviewed publications. DARPA sponsors fundamental and applied research in a variety of areas including data science, cyber, anomaly detection, etc., which may lead to experimental results and reusable technology designed to benefit multiple government domains.</p>
<p>The DARPA Open Catalog organizes publicly releasable material from DARPA programs. DARPA has an open strategy to help increase the impact of government investments.</p>
<p>DARPA is interested in building communities around government-funded software and research. If the R&D community shows sufficient interest, DARPA will continue to make available information generated by DARPA programs, including software, publications, data, and experimental results.</p></div>
<div id=''><p>The table on this page lists the programs currently participating in the catalog.</p>
<p>Program Manager:<br>
Dr. Christopher White<br>
<a href='mailto:christopher.white@darpa.mil'>christopher.white@darpa.mil</a></p>
<p>Report a problem: <a href="mailto:opencatalog@darpa.mil">opencatalog@darpa.mil</a></p>
<p>Last updated: """ 
  splash += date + "</p></div>"
  return splash
  
def splash_table_header():
  return """
<div style = 'width:100%; float:left;'><h2>Current Catalog Programs:</h2></div>
<table id='splash' class='tablesorter'> 
<thead> 
<tr> 
    <th>DARPA Program</th>
    <th>Office</th> 	
    <th>Description</th> 
</tr> 
</thead> 
<tbody> 
"""

def splash_table_footer():
  return """
</tbody> 
</table>
<br>
"""

def software_table_header(columns):
  header = "<table id='sftwr' class='tablesorter'>\n <thead>\n <tr>"
  for column in columns:
    header += "<th>%s</th>" % column
  header += "</tr>\n </thead>\n <tbody  class='list'>"
  return header

def table_footer():
  return """
</tbody> 
</table>
"""

def pubs_table_header(columns):

  header = "<table id='pubs' class='tablesorter'>\n <thead>\n <tr>"
  for column in columns:
    header += "<th>%s</th>" % column
  header += "</tr>\n </thead>\n <tbody  class='list'>"
  return header

def pubs_table_footer():
  return """
</tbody> 
</table>
<br>
"""

def project_banner(update_date, new_date, last_update_file, title):
  html = ""
  ribbon_class = ""
  ribbon_div = ""
  change_date = ""
  if new_date != "" and update_date != "":
    if new_date >= update_date:
     change_date = new_date
     ribbon_class = "ribbon-standard ribbon-red"
     ribbon_text = "NEW"
    else:
	  change_date = update_date
	  ribbon_class = "ribbon-standard ribbon-green"
	  ribbon_text = "UPD"
  elif new_date != "" and update_date == "":
    change_date = new_date
    ribbon_class = "ribbon-standard ribbon-red"
    ribbon_text = "NEW"
  elif update_date != "" and new_date == "":
    change_date = update_date
    ribbon_class = "ribbon-standard ribbon-green"
    ribbon_text = "UPD"
  f = open(last_update_file,"r")
  last_build_date = f.read()
  f.close()	
  if change_date > last_build_date:
    formatted_date = datetime.date.strftime(datetime.datetime.strptime(change_date, '%Y%m%d'), "%Y-%m-%d")  
    html = "<div class='wrapper'><div class='wrapper-text'>" + title + "</div><div class='ribbon-wrapper'><div class='"  + ribbon_class + "'>" + ribbon_text + " " + formatted_date + "</div></div></div>"
  else:
    html = title
  return html
  
def catalog_program_script(): 
  return """ 

<script type='text/javascript'>
var swList = pubList = spubList = ssftList = "";

$(document).ready(function() 
    { 
	   $('#sftwr').tablesorter({
		// sort on the first column and second column, order asc 
        	sortList: [[0,0],[1,0]] 
    	}); 
        $('#pubs').tablesorter({
        	sortList: [[0,0],[1,0]] 
    	});
        $('#splash').tablesorter({
		// sort on the first column, order asc 
        	sortList: [[0,0]] 
    	});
		
		//get the list of tabs and the number of tabs
		var tabList = $('#tabs >ul >li');
		var tabCount = $('#tabs >ul >li').size();
		
		//create table tabs
		$(function() {
			$( "#tabs" ).tabs
			var param_tab = decodeURIComponent(getUrlParams("tab"));
			var param_term = decodeURIComponent(getUrlParams("term"));
			if(param_tab == "false"){ 
				if($("#tabs0"))
					$("#tabs").tabs({active: 0}); //software tab
				else
					$("#tabs").tabs({active: 1}); //publications tab
			}
			else if(param_tab && param_term){
				if (param_tab == "tabs0")
					swSearch(param_term);
				else if (param_tab == "tabs1")
					pubSearch(param_term);
			}
			else{
				if (param_tab == "tabs0")
					$("#tabs").tabs({active: 0});  //software tab
				else if (param_tab == "tabs1")
					$("#tabs").tabs({active: 1});  //publications tab
			}

		});

		//configure table search and clear button for software and publications table
		for (var i=0; i<tabCount; i++){
			
			var tabName = tabList[i].textContent.toLowerCase(); //name of tab

			if(tabName == "software"){
				var tabTable = $('#tabs0 table'); //table within this tab
				var tabHeaders = getTableHeaders(tabTable);	
				
				var sw_options = {
				  valueNames: tabHeaders
				};
				
				swList = new List(tabName, sw_options);

				$("#clear0").click(function() {
					var currId = this.id.match(/\d+/g);
					$("#search" + currId[0]).val("");
					swList.search();
				});
			}
			
			if(tabName == "publications"){
				var tabTable = $('#tabs1 table'); //table within this tab
				var tabHeaders = getTableHeaders(tabTable);	
				
				var pub_options = {
				  valueNames: tabHeaders
				};

				pubList = new List(tabName, pub_options);

				$("#clear1").click(function() {
					var currId = this.id.match(/\d+/g);
					$("#search" + currId[0]).val("");
					pubList.search();
				});
				
			}
			
			if(tabName == "search"){

				var table_clone = $('#tabs table').clone();
				for (var k=0; k<table_clone.length; k++){
					var searchHeaders = getTableHeaders(table_clone[k]);
					var search_options = {
						  valueNames: searchHeaders
					};
					
					if (table_clone[k].id == "sftwr"){
						$("#softwareSearch #sftwrTable").append(table_clone[k]);
						//tables are hidden initially
						$("#softwareSearch #sftwrTable").hide();
						ssftList = new List("softwareSearch", search_options);					
					}
					else{
						$("#publicationsSearch #pubTable").append(table_clone[k]);
						$("#publicationsSearch #pubTable").hide();
						spubList = new List("publicationsSearch", search_options);
					}
					
				}

				$("#clear2").click(function() {
					var currId = this.id.match(/\d+/g);
					$("#search" + currId[0]).val("");
					if (ssftList != "")
						ssftList.search();
					if (spubList != "")
						spubList.search();
					//when search is cleared tables need to be hidden
					$("#softwareSearch #sftwrTable").hide();
					$("#publicationsSearch #pubTable").hide();
						
				});

			}
		}   
    } 
);

function jump(h){
    var url = location.href;
    location.href = "#"+h;
        history.replaceState(null,null,url)
}

function swSearch(link){
	console.log(link);
	var search_text = "";
	if(link.hash)
		search_text = link.hash.replace("#", "");
	else
		search_text = link;
	$('#tabs').tabs({active: 0}); //publications tab
	var search_box = $("#search0");
	search_box.val(search_text);

	setTimeout(function(){
		$('html, body').animate({
			scrollTop: $("#tabs").offset().top
		}, 0);
		search_box.focus();
		search_box.select();
		swList.search(search_text);
		
	},300);
}

function pubSearch(link){
	console.log(link);
	var search_text = "";
	if(link.hash)
		search_text = link.hash.replace("#", "");
	else
		search_text = link;
	$('#tabs').tabs({active: 1}); //publications tab
	var search_box = $("#search1");
	search_box.val(search_text);

	setTimeout(function(){
		$('html, body').animate({
			scrollTop: $("#tabs").offset().top
		}, 0);
		search_box.focus();
		search_box.select();
		pubList.search(search_text);		
	},300);
}

function allSearch(this_search){
	if(this_search.value != "" && this_search.value.length >= 3){
		var value = this_search.value; 
		//TODO: Implement Stop Words
		ssftList.search(value);
		
		//hide table if there are no rows that match the search term
		if ($("#softwareSearch #sftwrTable tbody").children().length != 0)
			$("#softwareSearch #sftwrTable").show();
		else
			$("#softwareSearch #sftwrTable").hide();
		
		if(spubList != ""){
			var value = this_search.value;
			spubList.search(value);
			
			if ($("#publicationsSearch #pubTable tbody").children().length != 0)
				$("#publicationsSearch #pubTable").show();
			else
				$("#publicationsSearch #pubTable").hide();
		}
	}
	else{
		//if search_term is empty or not 3 chars in length, make sure the tables are hidden
		$("#publicationsSearch #pubTable").hide();
		$("#softwareSearch #sftwrTable").hide();
	}
}

function getTableHeaders(table){
	var this_table;
	 
	if(table[0])
		this_table = table[0];
	else
		this_table = table;
		
	var headerRow = this_table.tHead.rows[0].cells; //header row of table
	var tableHeaders = [];

	for (var j=0; j<headerRow.length; j++) 
		tableHeaders.push(headerRow[j].textContent.toLowerCase());

	return tableHeaders;		
}

function licenseInfo(short_nm, long_nm, link, description, event){

	var x=event.clientX;
	var y=event.clientY;
	
	$( "#dialog" ).removeClass("ribbon-dialog");
	$(".ui-dialog").removeClass("ribbon-dialog vertical-green vertical-red");
	$(".ui-dialog-titlebar").removeClass("ribbon-dialog-text");
	
	if(short_nm != ""){
		$( "#dialog" ).empty().dialog({
		position: [x , y - 20],
		title: short_nm
		});

		if(description != "")
			$("#dialog").html("<a href='" + link + "'>" + long_nm + "</a>: " + description);
		else
			$("#dialog").html("<a href='" + link + "'>" + long_nm + "</a>");
	
		$(".ui-dialog").mouseleave( function () {
			 $( "#dialog" ).dialog( "close" );
		  });
	}
}

function getUrlParams(param_name)
{
       var query = window.location.search.substring(1);
       var params = query.split("&");
       for (var i=0;i<params.length;i++) {
               var pair = params[i].split("=");
               if(pair[0] == param_name){return pair[1];}
       }
       return(false);
}

function dateInfo(ribbon, event){
	if(ribbon !="")
	{
		var date_id = document.getElementById(ribbon).firstChild.id;
		var str_pattern = /(\d{4})(\d{2})(\d{2})/;
		var date = date_id.replace(str_pattern,"$2-$3-$1"); //full date string

		var ribbon_type = document.getElementById(ribbon).firstChild.getAttribute("name"); 
		var x=event.clientX;
		var y=event.clientY;
		var text = "";
		var background = "";
		
		if(ribbon_type == "NEW"){
			text = "CREATED";
			$(".ui-dialog").removeClass('vertical-green');
			background = "vertical-red";
		}
		else{
			text = ribbon_type;
			$(".ui-dialog").removeClass('vertical-red');
			background = "vertical-green";
		}

		$( "#dialog" ).empty().dialog({
		position: [x , y - 20],
		title: text + ": " + date,
		});		
		
		$( "#dialog" ).addClass("ribbon-dialog");
		$(".ui-dialog").addClass(background + " ribbon-dialog");
		$(".ui-dialog-titlebar").addClass("ribbon-dialog-text");
		


		$(".ui-dialog").mouseleave( function () {
			 $( "#dialog" ).dialog( "close" );
		});
	}
}
</script>
"""

def catalog_page_footer():
  return """
<footer>
<div class='footer-style'>
<hr>  
<p><a href='http://www.darpa.mil/FOIA.aspx'>FOIA</a> | <a href='http://www.darpa.mil/Privacy_Security_Notice.aspx'>Privacy and Security</a> | 
<a href='http://www.darpa.mil/NoFearAct.aspx'>No Fear Act</a> | <a href='http://www.darpa.mil/External_Link.aspx?url=http://dodcio.defense.gov/DoDSection508/Std_Stmt.aspx'>Accessibility/Section 508</a></p>
</div>
</footer>
</div>
</body>
</html>
"""

def write_file(html, file):
  page_file = file
  print "Writing to %s" % page_file
  outfile = open(page_file, 'w')
  outfile.write(html)

def valid_email(email, program):
  if re.match(r"^(([a-zA-Z0-9\-?\.?]+)@(([a-zA-Z0-9\-_]+\.)+)([a-z]{2,3}))+$", email)!=None:
    return email
  else: 
    raise ValueError( "%s is an invalid email address.  Please fix this in %s files and restart the build." % (email, program))
