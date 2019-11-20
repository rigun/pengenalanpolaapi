<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class AttendanceController extends Controller
{
    public function index(){
        return \DB::select('SELECT s.name, s.npm, s.id, a.created_at FROM students s JOIN attendances a ON s.id = a.student_id');
    }
}
