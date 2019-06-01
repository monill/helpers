<?php

function DownloadCurl($ch,$url, $folder, $headers, $encoded = true, $appand = true, $trueFilename = ''){

    $ch = $ch;
    if ($trueFilename != '') {
        echo 'downloading : ' . $trueFilename;
    } else {
        echo 'downloading : ' . @end(explode('/', $url));
    }

    set_time_limit(0);
    @mkdir(dirname(__FILE__) . '/' . $folder);
    $dest = dirname(__FILE__) . '/' . $folder.'/';

    curl_setopt($ch, CURLOPT_URL, $url);
    if ($encoded) {
        curl_setopt($ch, CURLOPT_ENCODING, "");
	}

    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

    $data = curl_exec($ch);

    $resp =$data;

    if ($resp === false) {
    	$down = false;
        echo 'Curl error: ' . /*curl_error($ch) .*/ PHP_EOL;
    } else {
        $httpCode = curl_getinfo($ch);
        if($httpCode['http_code'] == 404){
            echo "404 - Not Found".PHP_EOL;
            return false;
        }
        $urlFinal =  parse_url($httpCode['url']);
        parse_str($urlFinal['query'], $get_array);
        $re = '/filename="(.*)"/m';
        $str = $get_array['response-content-disposition'];

        preg_match_all($re, $str, $matches, PREG_SET_ORDER, 0);
        $filename = urldecode($matches[0][1]);

        if($httpCode['download_content_length'] == 0){
            $down = false;
            echo 'Curl error: ' . PHP_EOL;
        }else{
            file_put_contents($dest.$filename,$data);
            echo $filename;
            $down = true;
            echo ' - done'. PHP_EOL;
        }
    }

    return $down;

}

function openCh()
{
    //Here is the file we are downloading, replace spaces with %20
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 3);
    curl_setopt($ch, CURLOPT_TIMEOUT, 5);
    // curl_setopt($ch, CURLOPT_PROGRESSFUNCTION, 'progress');
    curl_setopt($ch, CURLOPT_NOPROGRESS, true); // needed to make progress function work
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    // get curl response

    return $ch;
}

$ch = openCh();

$headers = [
    'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Referer: https:///',
    'Origin: https:///',
];

$initialCount = 1;
$FinalCount = 1800000;
$linkMain = "";

for ($i=$initialCount; $i < $FinalCount; $i++) {
    $currentLink = str_replace('{{counter}}',$i,$linkMain);

    echo "$i: ";
    DownloadCurl($ch,$currentLink,"teste",$headers);

}
