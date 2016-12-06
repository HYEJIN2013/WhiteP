<?php
class string {
    protected $_src = null;

    public function __construct($src = '') {
        $this->_src = $src;
    }
    
    public function __toString() {
        return $this->_src;
    }
}

function foo(string $str) { echo($str); }

$test = new string('dupa');
foo($test);
?>