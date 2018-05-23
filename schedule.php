<div id="Schedule" class="tabcontent">
  <h3>Schedule</h3>
  <table id="scheduleTable" width=60%></table>
</div>


<script>

  var mondaySchedule=[];
  var tuesdaySchedule=[];
  var wednesdaySchedule=[];
  var thursdaySchedule=[];
  var fridaySchedule=[];
  var saturdaySchedule=[];
  var sundaySchedule=[];
  var Monday = "Monday";
  var Tuesday = "Tuesday";
  var Wednesday = "Wednesday";
  var Thursday = "Thursday";
  var Friday = "Friday";
  var Saturday = "Saturday";
  var Sunday = "Sunday";

  //initialize the schedule arrays
  function loadDay(schedule, time) {

    //if days are missing, don't try to load them
    if (typeof time !== 'undefined') {
          var times = time.split(",");

          var i;
          for(i = 0; i < times.length; i++) {
              schedule.push(times[i].trim().replace("[","").replace("]","").replace(" "," - "))
          }
        }

  }

  function updateScedule() {

    var tbl  = document.getElementById("scheduleTable");
    tbl.innerHTML = "<col width='10%'><col width='20%'><col width='70%'>";

    setDay("Monday", mondaySchedule, tbl);
    setDay("Tuesday", tuesdaySchedule, tbl);
    setDay("Wednesday", wednesdaySchedule, tbl);
    setDay("Thursday", thursdaySchedule, tbl);
    setDay("Friday", fridaySchedule, tbl);
    setDay("Saturday", saturdaySchedule, tbl);
    setDay("Sunday", sundaySchedule, tbl);

    var header = tbl.createTHead();
    var headerRow = header.insertRow();
    var th = headerRow.insertCell();
    th.innerHTML = "Day";
    th = headerRow.insertCell();
    th.innerHTML = "Record Times";

  }

  function setDay(dayName, schedule, table) {
    var tr = table.insertRow();
        var td = tr.insertCell();
        //td.innerHTML = "<input type='checkbox'>";
        //td = tr.insertCell();
        td.innerHTML = dayName;
        td = tr.insertCell();

        td.innerHTML = "<pre class=\"scheduleDisplay\"></pre>";
        var i;
        for(i = 0; i < schedule.length; i++) {
            td.children[0].innerHTML += schedule[i];
            td.children[0].innerHTML +="<span onclick=\"removeTimeslot("+dayName+","+i+")\" class=\"hidden\">&times</span>" + "\n";
        }
  }

  function removeTimeslot(day, slot) {

    var schedule;

    switch(day) {
      case "Monday":
        schedule = mondaySchedule;
        var toRemove = schedule[slot];
        mondaySchedule = schedule.filter(function(item) {return item !== toRemove});
        break;
      case "Tuesday":
        schedule = tuesdaySchedule;
        var toRemove = schedule[slot];
        tuesdaySchedule = schedule.filter(function(item) {return item !== toRemove});
        break;
      case "Wednesday":
        schedule = wednesdaySchedule;
        var toRemove = schedule[slot];
        wednesdaySchedule = schedule.filter(function(item) {return item !== toRemove});
        break;
      case "Thursday":
        schedule = thursdaySchedule;
        var toRemove = schedule[slot];
        thursdaySchedule = schedule.filter(function(item) {return item !== toRemove});
        break;
      case "Friday":
        schedule = fridaySchedule;
        var toRemove = schedule[slot];
        fridaySchedule = schedule.filter(function(item) {return item !== toRemove});
        break;
      case "Saturday":
        schedule = saturdaySchedule;
        var toRemove = schedule[slot];
        saturdaySchedule = schedule.filter(function(item) {return item !== toRemove});
        break;
      case "Sunday":
        schedule = sundaySchedule;
        var toRemove = schedule[slot];
        sundaySchedule = schedule.filter(function(item) {return item !== toRemove});
        break;
    }

    console.log(schedule);

    updateScedule();
  }

  function loadSchedule(evt) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById('Schedule').style.display = "block";
    evt.currentTarget.className += " active";

    //contact the blob storage
    blobService.getBlobToText('configuration', 'config.ini', function(error, text, result, response) {
      if (!error) {
        schedule_file = decode(text);
        console.log(schedule_file);

        loadDay(mondaySchedule, schedule_file.Schedule.monday);
        loadDay(tuesdaySchedule, schedule_file.Schedule.tuesday);
        loadDay(wednesdaySchedule, schedule_file.Schedule.wednesday);
        loadDay(thursdaySchedule, schedule_file.Schedule.thursday);
        loadDay(fridaySchedule, schedule_file.Schedule.friday);
        loadDay(saturdaySchedule, schedule_file.Schedule.saturday);
        loadDay(sundaySchedule, schedule_file.Schedule.sunday);

        updateScedule();
      }
    });
	}
</script>