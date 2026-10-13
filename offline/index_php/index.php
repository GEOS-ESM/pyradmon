<?php
?>
<html>
<head>
<title>Radiance Monitoring</title>

 <?php
  ini_set('display_errors', 'On');

  $datadir = 'radmon_data/';

  $insttable = array(
    "platform" => array(
      array("name" => "msu_tirosn",   "longname" => "MSU TIROS-N",    "nchan" => 4,   "startch" => 2,  "dosubset" => false),
      array("name" => "msu_n06",      "longname" => "MSU NOAA-6",     "nchan" => 4,   "startch" => 2,  "dosubset" => false),
      array("name" => "msu_n07",      "longname" => "MSU NOAA-7",     "nchan" => 4,   "startch" => 2,  "dosubset" => false),
      array("name" => "msu_n08",      "longname" => "MSU NOAA-8",     "nchan" => 4,   "startch" => 2,  "dosubset" => false),
      array("name" => "msu_n09",      "longname" => "MSU NOAA-9",     "nchan" => 4,   "startch" => 2,  "dosubset" => false),
      array("name" => "msu_n10",      "longname" => "MSU NOAA-10",    "nchan" => 4,   "startch" => 2,  "dosubset" => false),
      array("name" => "msu_n11",      "longname" => "MSU NOAA-11",    "nchan" => 4,   "startch" => 2,  "dosubset" => false),
      array("name" => "msu_n12",      "longname" => "MSU NOAA-12",    "nchan" => 4,   "startch" => 2,  "dosubset" => false),
      array("name" => "msu_n14",      "longname" => "MSU NOAA-14",    "nchan" => 4,   "startch" => 2,  "dosubset" => false),
      array("name" => "ssu_tirosn",   "longname" => "SSU TIROS-N",    "nchan" => 3,   "startch" => 1,  "dosubset" => false),
      array("name" => "ssu_n06",      "longname" => "SSU NOAA-6",     "nchan" => 3,   "startch" => 1,  "dosubset" => false),
      array("name" => "ssu_n07",      "longname" => "SSU NOAA-7",     "nchan" => 3,   "startch" => 1,  "dosubset" => false),
      array("name" => "ssu_n08",      "longname" => "SSU NOAA-8",     "nchan" => 3,   "startch" => 1,  "dosubset" => false),
      array("name" => "ssu_n09",      "longname" => "SSU NOAA-9",     "nchan" => 3,   "startch" => 1,  "dosubset" => false),
      array("name" => "ssu_n11",      "longname" => "SSU NOAA-11",    "nchan" => 3,   "startch" => 1,  "dosubset" => false),
      array("name" => "ssu_n14",      "longname" => "SSU NOAA-14",    "nchan" => 3,   "startch" => 1,  "dosubset" => false),
      array("name" => "amsua_n15",    "longname" => "AMSU-A NOAA-15", "nchan" => 15,  "startch" => 6,  "dosubset" => false),
      array("name" => "amsua_n16",    "longname" => "AMSU-A NOAA-16", "nchan" => 15,  "startch" => 6,  "dosubset" => false),
      array("name" => "amsua_n17",    "longname" => "AMSU-A NOAA-17", "nchan" => 15,  "startch" => 6,  "dosubset" => false),
      array("name" => "amsua_n18",    "longname" => "AMSU-A NOAA-18", "nchan" => 15,  "startch" => 6,  "dosubset" => false),
      array("name" => "amsua_n19",    "longname" => "AMSU-A NOAA-19", "nchan" => 15,  "startch" => 6,  "dosubset" => false),
      array("name" => "amsua_metop-a","longname" => "AMSU-A METOP-A", "nchan" => 15,  "startch" => 6,  "dosubset" => false),
      array("name" => "amsua_metop-b","longname" => "AMSU-A METOP-B", "nchan" => 15,  "startch" => 6,  "dosubset" => false),
      array("name" => "amsua_metop-c","longname" => "AMSU-A METOP-C", "nchan" => 15,  "startch" => 6,  "dosubset" => false),
      array("name" => "amsua_aqua",   "longname" => "AMSU-A Aqua",    "nchan" => 15,  "startch" => 6,  "dosubset" => false),
      array("name" => "atms_npp",     "longname" => "ATMS SNPP",      "nchan" => 22,  "startch" => 6,  "dosubset" => false),
      array("name" => "atms_n20",     "longname" => "ATMS N20",       "nchan" => 22,  "startch" => 6,  "dosubset" => false),
      array("name" => "atms_n21",     "longname" => "ATMS N21",       "nchan" => 22,  "startch" => 6,  "dosubset" => false),
      array("name" => "hirs2_tirosn", "longname" => "HIRS2 TIROS-N",  "nchan" => 19,  "startch" => 2,  "dosubset" => false),
      array("name" => "hirs2_n06",    "longname" => "HIRS2 NOAA-6",   "nchan" => 19,  "startch" => 2,  "dosubset" => false),
      array("name" => "hirs2_n07",    "longname" => "HIRS2 NOAA-7",   "nchan" => 19,  "startch" => 2,  "dosubset" => false),
      array("name" => "hirs2_n08",    "longname" => "HIRS2 NOAA-8",   "nchan" => 19,  "startch" => 2,  "dosubset" => false),
      array("name" => "hirs2_n09",    "longname" => "HIRS2 NOAA-9",   "nchan" => 19,  "startch" => 2,  "dosubset" => false),
      array("name" => "hirs2_n10",    "longname" => "HIRS2 NOAA-10",  "nchan" => 19,  "startch" => 2,  "dosubset" => false),
      array("name" => "hirs2_n11",    "longname" => "HIRS2 NOAA-11",  "nchan" => 19,  "startch" => 2,  "dosubset" => false),
      array("name" => "hirs2_n12",    "longname" => "HIRS2 NOAA-12",  "nchan" => 19,  "startch" => 2,  "dosubset" => false),
      array("name" => "hirs2_n14",    "longname" => "HIRS2 NOAA-14",  "nchan" => 19,  "startch" => 2,  "dosubset" => false),
      array("name" => "hirs3_n15",    "longname" => "HIRS3 NOAA-15",  "nchan" => 19,  "startch" => 2,  "dosubset" => false),
      array("name" => "hirs3_n16",    "longname" => "HIRS3 NOAA-16",  "nchan" => 19,  "startch" => 2,  "dosubset" => false),
      array("name" => "hirs3_n17",    "longname" => "HIRS3 NOAA-17",  "nchan" => 19,  "startch" => 2,  "dosubset" => false),
      array("name" => "hirs4_n18",    "longname" => "HIRS4 NOAA-18",  "nchan" => 19,  "startch" => 2,  "dosubset" => false),
      array("name" => "hirs4_n19",    "longname" => "HIRS4 NOAA-19",  "nchan" => 19,  "startch" => 2,  "dosubset" => false),
      array("name" => "hirs4_metop-a","longname" => "HIRS4 METOP-A",  "nchan" => 19,  "startch" => 2,  "dosubset" => false),
      array("name" => "hirs4_metop-b","longname" => "HIRS4 METOP-B",  "nchan" => 19,  "startch" => 2,  "dosubset" => false),
      array("name" => "airs_aqua",    "longname" => "AIRS Aqua",      "nchan" => 281, "startch" => 3,  "dosubset" => false),
      array("name" => "iasi_metop-a", "longname" => "IASI METOP-A",   "nchan" => 616, "startch" => 1,  "dosubset" => false),
      array("name" => "iasi_metop-b", "longname" => "IASI METOP-B",   "nchan" => 616, "startch" => 1,  "dosubset" => false),
      array("name" => "iasi_metop-c", "longname" => "IASI METOP-C",   "nchan" => 616, "startch" => 1,  "dosubset" => false),
      array("name" => "cris-fsr_npp", "longname" => "CRIS-FSR SNPP",  "nchan" => 431, "startch" => 1,  "dosubset" => false),
      array("name" => "cris-fsr_n20", "longname" => "CRIS-FSR N20",   "nchan" => 431, "startch" => 1,  "dosubset" => false),
      array("name" => "ssmi_f08",     "longname" => "SSMI F08",       "nchan" => 7,   "startch" => 1,  "dosubset" => false),
      array("name" => "ssmi_f10",     "longname" => "SSMI F10",       "nchan" => 7,   "startch" => 1,  "dosubset" => false),
      array("name" => "ssmi_f11",     "longname" => "SSMI F11",       "nchan" => 7,   "startch" => 1,  "dosubset" => false),
      array("name" => "ssmi_f13",     "longname" => "SSMI F13",       "nchan" => 7,   "startch" => 1,  "dosubset" => false),
      array("name" => "ssmi_f14",     "longname" => "SSMI F14",       "nchan" => 7,   "startch" => 1,  "dosubset" => false),
      array("name" => "ssmi_f15",     "longname" => "SSMI F15",       "nchan" => 7,   "startch" => 1,  "dosubset" => false),
      array("name" => "ssmis_f16",    "longname" => "SSMIS F16",      "nchan" => 24,  "startch" => 3,  "dosubset" => false),
      array("name" => "ssmis_f17",    "longname" => "SSMIS F17",      "nchan" => 24,  "startch" => 3,  "dosubset" => false),
      array("name" => "ssmis_f18",    "longname" => "SSMIS F18",      "nchan" => 24,  "startch" => 3,  "dosubset" => false),
      array("name" => "ssmis_f19",    "longname" => "SSMIS F19",      "nchan" => 24,  "startch" => 3,  "dosubset" => false),
      array("name" => "amsub_n15",    "longname" => "AMSU-B NOAA-15", "nchan" => 5,   "startch" => 1,  "dosubset" => false),
      array("name" => "amsub_n16",    "longname" => "AMSU-B NOAA-16", "nchan" => 5,   "startch" => 1,  "dosubset" => false),
      array("name" => "amsub_n17",    "longname" => "AMSU-B NOAA-17", "nchan" => 5,   "startch" => 1,  "dosubset" => false),
      array("name" => "mhs_n18",      "longname" => "MHS NOAA-18",    "nchan" => 5,   "startch" => 1,  "dosubset" => false),
      array("name" => "mhs_n19",      "longname" => "MHS NOAA-19",    "nchan" => 5,   "startch" => 1,  "dosubset" => false),
      array("name" => "mhs_metop-a",  "longname" => "MHS METOP-A",    "nchan" => 5,   "startch" => 1,  "dosubset" => false),
      array("name" => "mhs_metop-b",  "longname" => "MHS METOP-B",    "nchan" => 5,   "startch" => 1,  "dosubset" => false),
      array("name" => "mhs_metop-c",  "longname" => "MHS METOP-C",    "nchan" => 5,   "startch" => 1,  "dosubset" => false),
      array("name" => "sndr_g10",     "longname" => "GOES-10 SNDR",   "nchan" => 18,  "startch" => 1,  "dosubset" => false),
      array("name" => "sndr_g11",     "longname" => "GOES-11 SNDR",   "nchan" => 18,  "startch" => 1,  "dosubset" => false),
      array("name" => "sndr_g12",     "longname" => "GOES-12 SNDR",   "nchan" => 18,  "startch" => 1,  "dosubset" => false),        
      array("name" => "sndrd1_g11",   "longname" => "GOES-11 SNDR D1","nchan" => 18,  "startch" => 1,  "dosubset" => false),
      array("name" => "sndrd2_g11",   "longname" => "GOES-11 SNDR D2","nchan" => 18,  "startch" => 1,  "dosubset" => false),
      array("name" => "sndrd3_g11",   "longname" => "GOES-11 SNDR D3","nchan" => 18,  "startch" => 1,  "dosubset" => false),
      array("name" => "sndrd4_g11",   "longname" => "GOES-11 SNDR D4","nchan" => 18,  "startch" => 1,  "dosubset" => false),
      array("name" => "sndrd1_g12",   "longname" => "GOES-12 SNDR D1","nchan" => 18,  "startch" => 1,  "dosubset" => false),
      array("name" => "sndrd2_g12",   "longname" => "GOES-12 SNDR D2","nchan" => 18,  "startch" => 1,  "dosubset" => false),
      array("name" => "sndrd3_g12",   "longname" => "GOES-12 SNDR D3","nchan" => 18,  "startch" => 1,  "dosubset" => false),
      array("name" => "sndrd4_g12",   "longname" => "GOES-12 SNDR D4","nchan" => 18,  "startch" => 1,  "dosubset" => false),
      array("name" => "sndrd1_g13",   "longname" => "GOES-13 SNDR D1","nchan" => 18,  "startch" => 1,  "dosubset" => false),
      array("name" => "sndrd2_g13",   "longname" => "GOES-13 SNDR D2","nchan" => 18,  "startch" => 1,  "dosubset" => false),
      array("name" => "sndrd3_g13",   "longname" => "GOES-13 SNDR D3","nchan" => 18,  "startch" => 1,  "dosubset" => false),
      array("name" => "sndrd4_g13",   "longname" => "GOES-13 SNDR D4","nchan" => 18,  "startch" => 1,  "dosubset" => false),
      array("name" => "sndrd1_g14",   "longname" => "GOES-14 SNDR D1","nchan" => 18,  "startch" => 1,  "dosubset" => false),
      array("name" => "sndrd2_g14",   "longname" => "GOES-14 SNDR D2","nchan" => 18,  "startch" => 1,  "dosubset" => false),
      array("name" => "sndrd3_g14",   "longname" => "GOES-14 SNDR D3","nchan" => 18,  "startch" => 1,  "dosubset" => false),
      array("name" => "sndrd4_g14",   "longname" => "GOES-14 SNDR D4","nchan" => 18,  "startch" => 1,  "dosubset" => false),
      array("name" => "sndrd1_g15",   "longname" => "GOES-15 SNDR D1","nchan" => 18,  "startch" => 1,  "dosubset" => false),
      array("name" => "sndrd2_g15",   "longname" => "GOES-15 SNDR D2","nchan" => 18,  "startch" => 1,  "dosubset" => false),
      array("name" => "sndrd3_g15",   "longname" => "GOES-15 SNDR D3","nchan" => 18,  "startch" => 1,  "dosubset" => false),
      array("name" => "sndrd4_g15",   "longname" => "GOES-15 SNDR D4","nchan" => 18,  "startch" => 1,  "dosubset" => false),
      array("name" => "seviri_m08",   "longname" => "SEVIRI M08",     "nchan" => 8,   "startch" => 1,  "dosubset" => false),
      array("name" => "seviri_m09",   "longname" => "SEVIRI M09",     "nchan" => 8,   "startch" => 1,  "dosubset" => false),
      array("name" => "seviri_m10",   "longname" => "SEVIRI M10",     "nchan" => 8,   "startch" => 1,  "dosubset" => false),
      array("name" => "avhrr_n15",    "longname" => "AVHRR NOAA-15",  "nchan" => 3,   "startch" => 1,  "dosubset" => false),
      array("name" => "avhrr_n16",    "longname" => "AVHRR NOAA-16",  "nchan" => 3,   "startch" => 1,  "dosubset" => false),
      array("name" => "avhrr_n17",    "longname" => "AVHRR NOAA-17",  "nchan" => 3,   "startch" => 1,  "dosubset" => false),
      array("name" => "avhrr_n18",    "longname" => "AVHRR NOAA-18",  "nchan" => 3,   "startch" => 1,  "dosubset" => false),
      array("name" => "avhrr_n19",    "longname" => "AVHRR NOAA-19",  "nchan" => 3,   "startch" => 1,  "dosubset" => false),
      array("name" => "avhrr_metop-a","longname" => "AVHRR METOP-A",  "nchan" => 3,   "startch" => 1,  "dosubset" => false),
      array("name" => "avhrr_metop-b","longname" => "AVHRR METOP-B",  "nchan" => 3,   "startch" => 1,  "dosubset" => false),
      array("name" => "avhrr_metop-c","longname" => "AVHRR METOP-C",  "nchan" => 3,   "startch" => 1,  "dosubset" => false),
      array("name" => "gmi_gpm",      "longname" => "GMI GPM",        "nchan" => 13,  "startch" => 1,  "dosubset" => false),
      array("name" => "amsr2_gcom-w1","longname" => "AMSR2 GCOM-W1",  "nchan" => 14,  "startch" => 1,  "dosubset" => false),	
      array("name" => "tmi_trmm",     "longname" => "TRMM TMI",       "nchan" => 9,   "startch" => 1,  "dosubset" => false),	    
      array("name" => "amsre_aqua",   "longname" => "AMSRE Aqua",     "nchan" => 12,  "startch" => 1,  "dosubset" => false),
      )
   );

   $imgtype = array(
      array("fn_abbr" => "bkg", "longname" => "Observation Summary"),
      array("fn_abbr" => "anl", "longname" => "Analysis Summary"),
      array("fn_abbr" => "bcor","longname" => "Bias Correction"),
   );

   // Fix for PHP 8+: Ensure glob returns an array even if empty/false
   $explist = glob("$datadir/*", GLOB_ONLYDIR) ?: []; 
   
   if (!empty($explist)) {
       usort(
          $explist, function($a,$b){
             return (filemtime($a) - filemtime($b));
          }
       );
       $explist = array_reverse($explist);
       $explist = array_map('basename', $explist);
   }

   if (!isset($_POST['exp']) && !empty($explist)) {
      $_POST['exp'] = $explist[0];
   } elseif (isset($_POST['exp'], $_POST['oldexp']) && $_POST['exp'] <> $_POST['oldexp']) {
      unset($_POST['date']);
      unset($_POST['inst']);
   }
   
   if (!isset($_POST['imgtype'])) $_POST['imgtype'] = $imgtype[0]["fn_abbr"];
   $curexp = $_POST['exp'] ?? '';

   // Fix for PHP 8+
   $datelist = glob("$datadir/$curexp/*", GLOB_ONLYDIR) ?: [];
   
   if (!empty($datelist)) {
       $datelist = array_reverse($datelist);
       $datelist = array_map('basename', $datelist);
   }

   if (!isset($_POST['date']) && !empty($datelist)) {
      $_POST['date'] = $datelist[0];
   }
   $curdate = $_POST['date'] ?? '';

   // Fix for PHP 8+
   $instlist = glob("$datadir/$curexp/$curdate/*", GLOB_ONLYDIR) ?: [];
   if (!is_array($instlist)) $instlist = array($instlist);
   
   if (!empty($instlist)) {
       $instlist = array_map('basename', $instlist);
   }

   if (!isset($_POST['inst']) && !empty($instlist)) $_POST['inst'] = $instlist[0];
   if (!empty($instlist) && !in_array($_POST['inst'], $instlist)) $_POST['inst'] = $instlist[0];
   $curinst = $_POST['inst'] ?? '';

   $nchan = 1;
   $dosubset = false;

   foreach ($insttable["platform"] as $curplat) {
      if ($curplat['name'] == $curinst) {
         if (!isset($_POST['chan'])) $_POST['chan'] = $curplat['startch'];
         if ($_POST['chan'] > $curplat['nchan']) $_POST['chan'] = $curplat['startch'];
      }
   }

?>
</head>
<body>

<form action="index.php" method="post">


<table width="1342px;" >
  <tr>
    <td valign="top"> 

     <!-- Replaced deprecated HTML attributes with CSS. Removed width: 100% so it shrink-wraps -->
     <table style="border: 2px solid; padding: 6px; border-spacing: 8px;">
      <tr>
        <td colspan="2">
          <b>Statistics over Time and FOV</b>
        </td>
      </tr>
      <tr>
        <td colspan="2">
          <select name="date" style="width:100%" onchange="this.form.submit();">
          <?php
            foreach ($datelist as $date) {
               if ($curdate == $date) {
                  echo "  <option value={$date} selected>{$date}</option>\n";
               } else {
                  echo "  <option value={$date}>{$date}</option>\n";
               }
            }
          ?>
          </select>
        </td>
      </tr>
      <tr>
        <td colspan="2">
         <?php
            echo "<input type=hidden name=oldexp value={$curexp}>\n";
         ?>
         <select name="exp" style="width:100%" onchange="this.form.submit();">
          <?php
            foreach ($explist as $exp) {
               if ($curexp == $exp) {
                  echo "  <option value={$exp} selected>{$exp}</option>\n";
               } else {
                  echo "  <option value={$exp}>{$exp}</option>\n";
               }
            }
          ?>
          </select>
        </td>
      </tr>
      <tr>
        <td colspan="2">
          <select name="inst" style="width:100%" onchange="this.form.submit();">
          <?php
             $instsel = false;
             foreach ($instlist as $inst) {
                $instmatch = false;
                foreach ($insttable["platform"] as $curplat) {
                   if ($inst == $curplat['name']) {
                      $instmatch = true;
                      if ($curinst == $inst) {
                         echo "  <option value={$curplat['name']} selected>{$curplat['longname']}</option>\n";
                         $nchan    = $curplat['nchan'];
                         $dosubset = $curplat['dosubset'];
                         $instsel = true;
                      } else {
                         echo "  <option value={$curplat['name']}>{$curplat['longname']}</option>\n"; 
                      };
                   };
                };
                if (! $instmatch) echo "<br><br><br>WARNING: $inst not matched in table!!!<br><br><br>\n";
             };
             if (! $instsel && !empty($instlist)) {
                $curinst = $instlist[0];
                foreach ($insttable["platform"] as $curplat) {
                   if ($curinst == $curplat['name']) {
                      $nchan    = $curplat['nchan'];
                      $dosubset = $curplat['dosubset'];
                      $instsel = true;
                   }
                }
             };
          ?> 
          </select> 
        </td>
      </tr>
      <tr>
        <td colspan="2">
          <select name="chan" style="width:100%" onchange="this.form.submit();">
          <?php
             foreach (range(1, $nchan) as $chan) {
                if (isset($_POST['chan']) && $_POST['chan'] == $chan) {
                   echo "  <option value=$chan selected> Ch. $chan </option>\n";
                } else {
                   echo "  <option value=$chan > Ch. $chan </option>\n";
                }
             }
          ?>
          </select>
        </td>
      </tr>
      <tr>
        <td colspan="2">
          <select name="imgtype" style="width:100%" onchange="this.form.submit();">
          <?php
             foreach ($imgtype as $ctype) {
                if ($_POST['imgtype'] == $ctype["fn_abbr"]) {
                   echo "  <option value={$ctype["fn_abbr"]} selected> {$ctype["longname"]} </option>\n";
                } else {
                   echo "  <option value={$ctype["fn_abbr"]}> {$ctype["longname"]} </option>\n";
                }
             }
          ?>
          </select>
        </td>
      </tr>
      <tr>
        <td colspan="2">
          <div style="text-align: center;"> <!-- Replaced <center> -->
            <?php       
              $inst = $_POST['inst'] ?? '';
              $chan = $_POST['chan'] ?? 1;
              echo "<img src=\"/media/forecasts_systems/radmon/wf/{$inst}/wf_{$inst}_chan{$chan}.png\">\n";
            ?>
          </div>
        </td>
      </tr>
     </table>
    <td valign="top">
      <table style="border: 2px solid; padding: 6px; border-spacing: 8px;">
        <tr>
          <td valign="top">
             <div style="text-align: center;"> <!-- Replaced <center> -->
             <?php
                $exp = $_POST['exp'] ?? '';
                $date = $_POST['date'] ?? '';
                $imgtype_val = $_POST['imgtype'] ?? '';
                
                $img = "{$datadir}{$exp}/{$date}/{$inst}/{$inst}_{$imgtype_val}_ch{$chan}.png";
                echo "<a href=\"$img\">\n";
                echo "<img src=\"$img\" style=\"max-width: 100%; height: auto;\">\n" ;
                echo "</a>\n"
             ?>
             <br>
             <?php
                $curch  = $chan ; 
                $prevch = $chan - 1;
                $nextch = $chan + 1;
                if ($curch > 1) { 
                   echo "<button name=\"chan\" type=\"submit\" value=\"$prevch\">Prev Channel</button>" ;
                }
                if ($curch < $nchan) { 
                   echo "<button name=\"chan\" type=\"submit\" value=\"$nextch\">Next Channel</button>" ;
                }
             ?>
             </div>
          </td>
        </tr> <!-- Fixed missing closing tr -->
      </table>
    </td>
  </tr>
</table>

</form>
</body></html>

