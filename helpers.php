<?php

if (!function_exists('getIP')) {
    function getIP() {
        // check for shared internet/ISP IP
        if (!empty($_SERVER['HTTP_CLIENT_IP']) && validIP($_SERVER['HTTP_CLIENT_IP'])) {
            return $_SERVER['HTTP_CLIENT_IP'];
        }
        // check for IPs passing through proxies
        if (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
            // check if multiple ips exist in var
            if (strpos($_SERVER['HTTP_X_FORWARDED_FOR'], ',') !== false) {
                $iplist = explode(',', $_SERVER['HTTP_X_FORWARDED_FOR']);
                foreach ($iplist as $ip) {
                    if (validIP($ip)) {
                        return $ip;
                    }
                }
            } else {
                if (validIP($_SERVER['HTTP_X_FORWARDED_FOR'])) {
                    return $_SERVER['HTTP_X_FORWARDED_FOR'];
                }
            }
        }
        if (!empty($_SERVER['HTTP_X_FORWARDED']) && validIP($_SERVER['HTTP_X_FORWARDED'])) {
            return $_SERVER['HTTP_X_FORWARDED'];
        }
        if (!empty($_SERVER['HTTP_X_CLUSTER_CLIENT_IP']) && validIP($_SERVER['HTTP_X_CLUSTER_CLIENT_IP'])) {
            return $_SERVER['HTTP_X_CLUSTER_CLIENT_IP'];
        }
        if (!empty($_SERVER['HTTP_FORWARDED_FOR']) && validIP($_SERVER['HTTP_FORWARDED_FOR'])) {
            return $_SERVER['HTTP_FORWARDED_FOR'];
        }
        if (!empty($_SERVER['HTTP_FORWARDED']) && validIP($_SERVER['HTTP_FORWARDED'])) {
            return $_SERVER['HTTP_FORWARDED'];
        }
        // return unreliable ip since all else failed
        return $_SERVER['REMOTE_ADDR'];
    }
}

if (!function_exists('validIP')) {
    function validIP($ip) {
        if (strtolower($ip) === "ip_unknown") {
            return false;
        }
        // generate ipv4 network address
        $ip = ip2long($ip);
        // if the ip is set and not equivalent to 255.255.255.255
        if ($ip !== false && $ip !== -1) {
            // make sure to get unsigned long representation of ip due to discrepancies
            // between 32 and 64 bit OSes and signed numbers (ints default to signed in PHP)
            $ip = sprintf("%u", $ip);
            // do private network range checking
            if ($ip >= 0 && $ip <= 50331647) {
                return false;
            }
            if ($ip >= 167772160 && $ip <= 184549375) {
                return false;
            }
            if ($ip >= 2130706432 && $ip <= 2147483647) {
                return false;
            }
            if ($ip >= 2851995648 && $ip <= 2852061183) {
                return false;
            }
            if ($ip >= 2886729728 && $ip <= 2887778303) {
                return false;
            }
            if ($ip >= 3221225984 && $ip <= 3221226239) {
                return false;
            }
            if ($ip >= 3232235520 && $ip <= 3232301055) {
                return false;
            }
            if ($ip >= 4294967040) {
                return false;
            }
        }
        return true;
    }
}

if (!function_exists('md5Gen')) {
    function md5Gen() {
        return md5(uniqid() . time() . microtime());
    }
}

if (!function_exists('makeSize')) {
    function makeSize($bytes, $decimals = 2) {
        $size = [' B', ' kB', ' MB', ' GB', ' TB', ' PB', ' EB', ' ZB', ' YB'];
        $floor = floor((strlen($bytes)-1)/3);
        return sprintf("%.{$decimals}f", $bytes/pow(1024, $floor)).@$size[$floor];
    }
}

if (!function_exists('sha1Gen')) {
    function sha1Gen() {
        return sha1(uniqid() . time() . microtime() . str_random(10));
    }
}

if (!function_exists('diaMesAno')) {
    function diaMesAno() {
        setlocale(LC_TIME, 'pt_BR', 'pt_BR.utf-8', 'pt_BR.utf-8', 'portuguese');
        date_default_timezone_set('America/Sao_Paulo');
        return strftime('%A, %d de %B de %Y', strtotime('today'));
    }
}

if (!function_exists('ytVideo')) {
    function ytVideo() {
        if ($this->video1 != null) {
            $url = $this->video1;

            if ($this->checkUrl($url)) {
                $fetch = explode("v=", $url);
                $videoId = $fetch[1];

                return $this->videoImage($videoId);
            }
        }
    }
}

if (!function_exists('videoImage')) {
    function videoImage($videoId) {
        if ($this->checkUrl('https://i.ytimg.com/vi/' . $videoId . '/maxresdefault.jpg')) {
            return 'https://i.ytimg.com/vi/' . $videoId . '/maxresdefault.jpg';
        } elseif ($this->checkUrl('https://img.youtube.com/vi/' . $videoId . '/maxresdefault.jpg"')) {
            return 'https://img.youtube.com/vi/' . $videoId . '/maxresdefault.jpg"';
        } else {
            return asset('site/assets/images/no-image-found.png');
        }
    }
}

//gerar arquivos de 100k em 100k
$filename = 'arquivo.{{id}}.txt';

for ($i=100000; $i<=2000000; $i+=100000) {
    // str_replace('{{id}}', $i, $filename);
    echo touch(str_replace('{{id}}', $i, $filename)) . '<br>';
}

if (!function_exists('url')) {
    function url($link)
    {
        $url = (isset($_SERVER['HTTPS']) ? "https" : "http") . "://$_SERVER[HTTP_HOST]";
        return $url . "/$link";
    }
}
if (!function_exists('asset')) {
    function asset($file)
    {
        $url = (isset($_SERVER['HTTPS']) ? "https" : "http") . "://$_SERVER[HTTP_HOST]";
        return $url . "/$file";
    }
}
