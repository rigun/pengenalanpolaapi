<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Student extends Model
{
    public function pictures(){
        return $this->hasMany('App\Picture','student_id','id');
    }
    public function myclass(){
        return $this->belongsToMany('App\ClassDesc','student_classes','student_id','class_id');
    }
}
