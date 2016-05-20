<?php
  $servername = "127.0.0.1";
  $username = "root";
  $password = "trung";
  $dbname = "MonitoringDB";

  $conn = mysqli_connect($servername, $username, $password, $dbname);
  if (!$conn) {
      die("Connection failed: " . mysqli_connect_error());
  }
  $rows = array(); 
  $table = array(); 
  $table['cols'] = array(
    array('label' => 'Time', 'type' => 'string'),
    array('label' => 'Die', 'type' => 'number'),
    array('label' => 'Live', 'type' => 'number')
    );
    $rows = array();
    $temp = array();
    $sqltime ="SELECT Time AS Times FROM inserttable GROUP BY Time";
    $result = mysqli_query($conn, $sqltime);

    if (mysqli_num_rows($result) > 0) {
      $s = array();
      $x =0;
      while($row = mysqli_fetch_assoc($result)) {
            $s[$x] = $row['Times'];
            $x=$x+1;
        }
    } else {
        echo "0 results";
    }
    #echo count($s);
    for($r=count($s)-1;$r>=count($s)-12;$r--){
        //echo $s[$r]."<br>";
        $temp = array();
        
        $temp[] = array('v' => $s[$r]);
        
        $sqldie ="SELECT COUNT(Ids) AS Die FROM `inserttable` WHERE Active=1 and Time=\"$s[$r]\"";
        $result = mysqli_query($conn, $sqldie);
        if (mysqli_num_rows($result) > 0) {
          while($row = mysqli_fetch_assoc($result)) {
                $temp[] = array('v' => (int) $row['Die']);
            }
        } else {
            echo "0 results";
        }

        $sqllive ="SELECT COUNT(Ids) AS Live FROM `inserttable` WHERE Active=0 and Time=\"$s[$r]\"";
        $result = mysqli_query($conn, $sqllive);

        if (mysqli_num_rows($result) > 0) {
          while($row = mysqli_fetch_assoc($result)) {
                $temp[] = array('v' => (int) $row['Live']);
            }
        } else {
            echo "0 results";
        }
        $rows[] = array('c' => $temp);
    }
    $table['rows'] = $rows;
    $jsonTable = json_encode($table);
    //echo $jsonTable;
  mysqli_close($conn);

?>
<html>
  <head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawVisualization);


      function drawVisualization() {
      var data = new google.visualization.DataTable(<?=$jsonTable?>);

      var options = {
      title : 'List Website Die and Live in Database.',
      vAxis: {title: 'Number of Website'},
      hAxis: {title: 'Time Current'},
      seriesType: 'bars',
      series: {5: {type: 'line'}}
    };

    var chart = new google.visualization.ComboChart(document.getElementById('chart_div'));
    chart.draw(data, options);
  }
    </script>
  </style>
  </head>
  <body>
        <div id="chart_div" style="width: 1200px; height: 500px;"></div>
  </body>
</html>
