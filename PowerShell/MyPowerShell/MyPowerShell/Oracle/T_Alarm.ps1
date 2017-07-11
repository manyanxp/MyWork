#------------------------------------------------------------
# PowerShell Version: 4.0以降
# Oracle Version    : Oracle 12c
#------------------------------------------------------------
Set-ExecutionPolicy Bypass

#connect oracle
[void][System.Reflection.Assembly]::LoadFile("C:\DRRApp\DataProcess\Oracle.DataAccess.dll")

#Oracleへのアクセス情報
$constr = "User ID=kyosan_db; Password=Orlando_DB0; Data Source=OrlandoDB;DBA privilege=SYSDBA"
$sqlStr = @("select * from KYOSAN_DB.t_alarm")

#Oracleへ接続
$conn = New-Object Oracle.DataAccess.Client.OracleConnection( $constr )
$conn.Open()

#OracleへSelect文を発行
$cmd = New-Object Oracle.DataAccess.Client.OracleCommand
$cmd.Connection = $conn
$cmd.CommandText = $sqlStr

$reader = $cmd.ExecuteReader()

#$title = ""
#for($counter = 0; $counter -le 20; $counter++)
#{
#    $title += $reader.getName($counter) 
#}

#"$title"

#while( $reader.read() )
#{
#    "-----------------------------------------"
#    $reader[1]
#}

#$cmd.Dispose()


$major = 0
$sub = 0
$detail = 0

$txn = $conn.BeginTransaction()
# Insert文を指定数文発行
for( $seq = 1; $seq -le 100000; $seq++)
{
    "Seq" + $seq

    $major = [byte] $major
    $sub = [byte] $sub
    $detail = [byte] $detail

    Start-Sleep -m 5

    $adddate = (Get-Date).AddSeconds($seq)
    $adddate = $adddate.AddDays(-1)
    $date = $adddate.year.ToString() +"/"+$adddate.month.ToString()+"/"+$adddate.day.ToString()
    $time = $adddate.hour.ToString()+":"+$adddate.minute.ToString()+":"+$adddate.second.ToString()

    #$insert = "INSERT INTO KYOSAN_DB.t_alarm (SEQ_NO,ATS_DEVICE_ID,SEQ_TIME,OCCURRED_TIME,ACKNOW_TIME,RESTORED_TIME,MAJOR_CODE,SUB_CODE,DETAIL_CODE,LOCATION_CODE_1,LOCATION_CODE_2,LOCATION_CODE_3,LOCATION_CODE_4,LOCATION_CODE_5,LOCATION_CODE_6,LOCATION_CODE_7,LOCATION_CODE_8,POS_KIND,TRAIN_NO,DESC_CODE, OPE_ROUTE_CODE) VALUES("+ $seq + ",1,TO_DATE('"+$date+" "+$time+"','YYYY-MM-DD HH24:MI:SS'),TO_DATE('"+$date+" "+$time+"','YYYY-MM-DD HH24:MI:SS'),TO_DATE('"+$date+" "+$time+"','YYYY-MM-DD HH24:MI:SS'),TO_DATE('"+$date+" "+$time+"','YYYY-MM-DD HH24:MI:SS'),'"+$major+"','"+$sub+"','"+$detail+"','0000000000000000','0000000000000000','0000000000000000','0000000000000000','0000000000000000','0000000000000000','0000000000000000','0000000000000000','00','8000000000000015','01','02')"
	$insert = "INSERT INTO KYOSAN_DB.t_alarm (SEQ_NO,ATS_DEVICE_ID,SEQ_TIME,OCCURRED_TIME,ACKNOW_TIME,RESTORED_TIME,MAJOR_CODE,SUB_CODE,DETAIL_CODE,LOCATION_CODE_1,LOCATION_CODE_2,LOCATION_CODE_3,LOCATION_CODE_4,LOCATION_CODE_5,LOCATION_CODE_6,LOCATION_CODE_7,LOCATION_CODE_8,POS_KIND,TRAIN_NO,DESC_CODE, OPE_ROUTE_CODE) VALUES("+ $seq + ",1,TO_DATE('"+$date+" "+$time+"','YYYY-MM-DD HH24:MI:SS'),TO_DATE('"+$date+" "+$time+"','YYYY-MM-DD HH24:MI:SS'),TO_DATE('"+$date+" "+$time+"','YYYY-MM-DD HH24:MI:SS'),TO_DATE('"+$date+" "+$time+"','YYYY-MM-DD HH24:MI:SS'),'02','11','0006','0100000000000001','0000000000000000','0000000000000000','0000000000000000','0000000000000000','0000000000000000','0000000000000000','0000000000000000','00','8000000000000015','01','02')"
    #$insert
    $cmd.Connection = $conn
    $cmd.CommandText = $insert
    $cmd.ExecuteNonQuery()

}
$txn.Commit()

$cmd.Dispose()

$conn.Close()
$conn.Dispose()