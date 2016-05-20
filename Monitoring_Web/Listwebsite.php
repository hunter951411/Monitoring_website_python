<?php
		$page = $_SERVER['PHP_SELF'];
		$sec = "300";
		$servername = "127.0.0.1";
		$username = "root";
		$password = "trung";
		$dbname = "MonitoringDB";
		$conn = mysqli_connect($servername, $username, $password, $dbname);
		if (!$conn) {
		      die("Connection failed: " . mysqli_connect_error());
		}
		if (isset($_GET['addtext']))
		{
	      		$url = $_GET['addtext'];
	      		$sqladd = "Insert into `updatetable`(Url) values('$url')";
	      		$resultadd = mysqli_query($conn, $sqladd) or die("Error in Selecting " . mysqli_error($conn));
	    }
		if (isset($_GET['delete']))
		{
	      		$delete = $_GET['delete'];
	      		$sqldelete = "Delete FROM `updatetable` WHERE Ids =$delete";
	      		$resultdelete = mysqli_query($conn, $sqldelete) or die("Error in Selecting " . mysqli_error($conn));
	    }
		if (isset($_GET['id']))
		{
	      		$id = $_GET['id'];
	    	}else{
	      		$id = 1;
    		}
		
		
  		$sql1 = "SELECT Url FROM `updatetable` WHERE Ids =$id";
   		$result1 = mysqli_query($conn, $sql1) or die("Error in Selecting " . mysqli_error($conn)); 
		while($r1 =mysqli_fetch_assoc($result1))
		{ 
		  $url =  $r1['Url'];	
		}
		$rows = array(); 
		$table = array(); 
		$table['cols'] = array(
		array('label' => 'Time', 'type' => 'string'),
		array('label' => 'PingTime', 'type' => 'number'),
		array('label' => 'GetTime', 'type' => 'number')
		);
		$rows = array();
		if (isset($_GET['search'])){
			$fromdate = $_GET['startdate'];
			$todate = $_GET['enddate'];
			$sql2 = "SELECT Pingtime, GetTime, Time FROM `inserttable` WHERE Url =\"$url\" AND Time BETWEEN '$fromdate' AND '$todate'";
		}else{
			$sql2 = "SELECT PingTime, GetTime, Time FROM `inserttable` WHERE Url =\"$url\" AND Time BETWEEN '2016-05-06 10:13:00' AND '2016-05-06 10:15:00'";
		}
		$result2 = mysqli_query($conn, $sql2) or die("Error in Selecting " . mysqli_error($conn)); 
		if (mysqli_num_rows($result2) > 0) {
			while($r2 =mysqli_fetch_assoc($result2))
			{
			  $temp = array();
			  $temp[] = array('v' => $r2['Time']);
			  $temp[] = array('v' => (int) $r2['PingTime']);
			  $temp[] = array('v' => (int) $r2['GetTime']);
			  $rows[] = array('c' => $temp);
			}
		} else {
			echo "0 results";
		}
		$table['rows'] = $rows;
		$jsonTable = json_encode($table);
  		mysqli_close($conn);
?>
<html>
<head>
	<meta http-equiv="refresh" content="<?php echo $sec?>;URL='<?php echo $page?>'" Content-Type="text/css; charset=utf-8">
	<link rel="stylesheet" href="listwebsite.css">
	<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['corechart']});

      google.charts.setOnLoadCallback(drawVisualization);


      function drawVisualization($i) {
      //alert($i);
      var data = new google.visualization.DataTable(<?=$jsonTable?>);
      var options = {
          chart: {
            title: 'ColumnChart List Time Ping Reply and Get Reply in Database.',
            colors: ["red", "green"]
          }
        };
        var chartColumn = new google.visualization.ColumnChart(document.getElementById('chart_div'));
        chartColumn.draw(data, options);
      if($i==1){
        var options = {
          chart: {
            title: 'ColumnChart List Time Ping Reply and Get Reply in Database.',
          }
        };
        var chartColumn = new google.visualization.ColumnChart(document.getElementById('chart_div'));
        chartColumn.draw(data, options);
      }else if($i==2){
        var options = {
          title: 'LineChart List Time Ping Reply and Get Reply in Database.',
          curveType: 'function',
          legend: { position: 'bottom' }
        };
        var chartLine = new google.visualization.LineChart(document.getElementById('chart_div'));
        chartLine.draw(data, options);
      }else if($i==3){
        var options = {
        title : 'ComboChart List Time Ping Reply and Get Reply in Database.',
        vAxis: {title: 'Time in (s)'},
        hAxis: {title: 'Time Current'},
        seriesType: 'bars',
        series: {5: {type: 'line'}}
        };
          var chartCombo = new google.visualization.ComboChart(document.getElementById('chart_div'));
          chartCombo.draw(data, options);
        var options = {
          title: 'ComboChart List Time Ping Reply and Get Reply in Database.',
          hAxis: {title: 'Time Current',  titleTextStyle: {color: '#333'}},
          vAxis: {minValue: 0}
        };

        var chart = new google.visualization.AreaChart(document.getElementById('chart_div'));
        chart.draw(data, options);   
      }
    }


      </script>
	<title>List Website Demo</title>
</head>
<body>
    <div align="center">
    <div class="bhtw"><h2>Bang hien thi website</h2></div>
		<div class="add"><h3><form><input type="text" name="addtext" placeholder="Nhap ten website can them">&nbsp;<input type="submit" name="add" value="ADD"></form></h3></div>
		<div  class="searchdate"><form>From:&nbsp;<input type="text" name="startdate" placeholder="2016-04-11 20:00:00">&nbsp;&nbsp;To:&nbsp;<input type="text" name="enddate" placeholder="2016-04-11 20:30:00">&nbsp;&nbsp;<input type="submit" name="search" value="Search"></form></div>
		<table cellspacing="0" cellpadding="1", width="870" border="0">
			<tr>
				<td>
					<table cellspacing="0" cellpadding="1" border="1" width="870">
						<tr style="color:white;background-color:red;font-weight:bold;font-family:verdana;">
							<td class="id">ID</td>
							<td class="url">URL</td>
							<td class="pingreply">Ping Reply</td>
							<td class="getreply">Get Reply</td>
							<td class="active">Active</td>
							<td class="time">Time</td>
							<td class="action">Action</td>
						</tr>
					</table>
				</td>
			</tr>
			<tr>
				<td>
					<div style="width:880px; height:150px; overflow:auto;">
						<table cellspacing="0" cellpadding="1" border="1" width="870" style="background-color:#00FFFF">
								<?php 
									$servername = "127.0.0.1";
									$username = "root";
									$password = "trung";
									$dbname = "MonitoringDB";
									$conn = mysqli_connect($servername, $username, $password, $dbname);
									if (!$conn) {
									      die("Connection failed: " . mysqli_connect_error());
									}
									$sql = "SELECT * FROM `updatetable`";
									$result = mysqli_query($conn, $sql) or die("Error in Selecting " . mysqli_error($conn)); 
									while($r =mysqli_fetch_assoc($result))
									{
									    $id = $r['Ids'];
									    $url = $r['Url'];
									    $pingreply = $r['LastPingTime'];
									    $getreply = $r['LastGetTime'];
									    $active = $r['Active'];
									    $time =$r['LastTime'];
									    ?>
										<tr>
											<td class="id"><?php echo $id; ?></td>
										    <td class="url"><?php echo $url; ?></td>
										    <td class="pingreply"><?php echo $pingreply; ?></td>
										    <td class="getreply"><?php echo $getreply; ?></td>
										    <td class="active"><?php echo $active; ?></td>
										    <td class="time"><?php echo $time; ?></td> 
										    <td class="action"><a href="Listwebsite.php?id=<?php echo $id; ?>">Detail</a>&nbsp;|&nbsp;<a href="pages/edit.php?id=<?php echo $id; ?>">Edit</a>&nbsp;|&nbsp;<a href="Listwebsite.php?delete=<?php echo $id; ?>">Delete</a></td>
										</tr>
								<?php }
								?>
						</table>
					</div>
				</td>
			</tr>
		</table>
		<div class="dht">
		<h3 align=\"center\">Thong tin website <?php echo $url;?></h3>
		<strong>Dang hien thi:&nbsp;</strong><Select id="selectBox" onchange="drawVisualization(value);">
											<option value="1">--Column--</option>
											<option value="2">--Line--</option>
											<option value="3">--Combo--</option></Select></div>
		<div class="chart_div" id="chart_div"></div>
		</div>
</body>
</html>
