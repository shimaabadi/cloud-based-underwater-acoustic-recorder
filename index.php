<html>
<style>
/* Header containing the logo*/
.header {
    height: 210px;
    background:#F0F0F0;
    border:1px solid #CCC;
    margin:0px auto;
}

.container {
	border:2px solid #ccc;
	width:100%;
	height:50%;
	overflow-y: scroll;
	}

	/* Style the tab */
.tab {
    overflow: hidden;
    border: 1px solid #ccc;
    background-color: #f4f4f4;
}

/* Style the buttons inside the tab */
.tab button {
    background-color: inherit;
    float: left;
    border: none;
    outline: none;
    cursor: pointer;
    padding: 14px 16px;
    transition: 0.3s;
    font-size: 17px;
}

/* Change background color of buttons on hover */
.tab button:hover {
    background-color: #ddd;
}

/* Create an active/current tablink class */
.tab button.active {
    background-color: #ccc;
}

/* Style the tab content */
.tabcontent {
    display: none;
    padding: 6px 12px;
    border-top: none;
}

#scheduleTable thead {
    padding-top: 12px;
    padding-bottom: 12px;
    text-align: left;
    background-color: #4CAF50;
    color: white;
}

#scheduleTable td{
    border: 1px solid #ddd;
    padding: 8px;
}

#scheduleTable tbody tr:nth-child(odd){background-color: #f2f2f2;}
#scheduleTable tbody tr:nth-child(even){background-color: #e2e2e2;}

.scheduleDisplay {
    line-height: 200%;
    font-size: 16px;
}

/* Style the close button */
.hidden {
    margin-left:20px;
    cursor: pointer;
    display:none;
    font-size: 16px;
}

.scheduleDisplay:hover .hidden { display:inline; }

.hidden:hover {color: red;}
</style>
<?php
	$maxcols = 5;
?>
 <head>
<title>CUAR</title>
  <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
  <script src="scripts/azure-storage.blob.js"></script>
  <script src="scripts/ini.js"></script>
  <script>
    var schedule_file;
    // Blob-related code goes here

	  const account = {
      name: 'cuartest',
      sas:  'se=2118-05-09T00%3A00%3A00Z&sp=rwdlac&sv=2017-07-29&ss=b&srt=sco&sig=CK/oHeN5SvFXYc49VyPba8bgIXqQFW2vAIz45NhYhwg%3D'
    };

    const blobUri = 'https://' + account.name + '.blob.core.windows.net';
    const blobService = AzureStorage.Blob.createBlobServiceWithSas(blobUri, account.sas);
  </script>
 </head>
 <body>
	<div class="header" align="center"><img src="logo.png" alt="logo" /></div>
	<div class="tab">
  <button class="tablinks" onclick="openCity(event, 'Status')" id="defaultOpen">Status</button>
  <button class="tablinks" onclick="loadSchedule(event)">Schedule</button>
  <button class="tablinks" onclick="openCity(event, 'Downloads')">Downloads</button>
</div>

<?php include 'status.php';?>
<?php include 'schedule.php';?>
<?php include 'downloads.php';?>

<script>
function openCity(evt, cityName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
	}

	// Get the element with id="defaultOpen" and click on it
	document.getElementById("defaultOpen").click();
</script>
 </body>
</html>