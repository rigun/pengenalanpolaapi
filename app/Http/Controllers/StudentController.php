<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Student;
use App\Picture;

class StudentController extends Controller
{  
    private $photos_path;

    public function __construct()
    {
        $this->photos_path = public_path('/picture');

    }
    public function index(){
        return Student::all();
    }
    
    public function update(Request $request, $id){
        $this->validateWith([
            'name' => 'required'
        ]);

        $item = Student::findorfail($id);
        $item->name = $request->name;
        $item->save();
        return response()->json(['msg' => 'berhasil', 'color' => 'green']);

    }
    public function destroy($id){
        $student = Student::findOrFail($id);
        \File::deleteDirectory(public_path('/model/pictures').'/'.$student->npm);
        if(file_exists(public_path('/model/realPict').'/'.$student->npm.'.jpg')){
            unlink(public_path('/model/realPict').'/'.$student->npm.'.jpg');
        }
        $student->delete();
        $filehandling = public_path("/model/trainFileHandling.txt");
        $myfile = fopen($filehandling, "r") or die("Unable to open file!");
        $num_clases = fread($myfile,filesize($filehandling));
        fclose($myfile);
        $num_clases -= 1;
        $myfile  = fopen($filehandling, "w");
        fwrite($myfile, $num_clases);
        fclose($myfile);
        return response()->json(['msg' => 'berhasil', 'color' => 'green']);
    }

}
