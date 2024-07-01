<?php

  //To be changed
  $receiving_email_address = 'info@masterheattechnology.com';

  if($_POST['_wpcf7_unit_tag'] == 'wpcf7-f271-o1'){
    $from = $_POST['client-name'].' '.$_POST['client-surname'] .'<'. $_POST['email'] .'>';
    $subject = $_POST['subject'];
    $message = "" .
              "Name:" . $_POST['client-name'].' '.$_POST['client-surname'] . "\r\n" .
              "Email:" . $_POST['email'] . "\r\n" .
              "Phone:" . $_POST['phone'] . "\r\n" .
              "Company Name:" . $_POST['company'] . "\r\n" .
              "Comapny Address:" . $_POST['address'] . "\r\n" .
              "Country:" . $_POST['country'] . "\r\n" .
              "Request:" . $_POST['request'] . "\r\n";
  } else {
    $from = $_POST['nome-cognome'] .'<'. $_POST['email'] .'>';
    $subject = "Catalogue Download Request - " . $_POST['company'];
    $message = "" .
              "Name:" . $_POST['nome-cognome']. "\r\n" .
              "Email:" . $_POST['email'] . "\r\n" .
              "Company:" . $_POST['company'] . "\r\n";
  }

  $from = $_POST['name'] .'<'. $_POST['email'] .'>';
  $headers = "" .
           "Reply-To:" . $from . "\r\n" .
           "From:" . $from . "\r\n" .
           "X-Mailer: PHP/" . phpversion();
  $headers .= 'MIME-Version: 1.0' . "\r\n";
  $headers .= 'Content-type: text/html; charset=iso-8859-1' . "\r\n"; 
  echo mail($receiving_email_address, $subject, $message, $headers);
?>
