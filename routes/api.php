<?php

use Illuminate\Http\Request;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| is assigned the "api" middleware group. Enjoy building your API!
|
*/

header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Headers: *');
header('Access-Control-Allow-Methods: *');
Route::group(['middleware' => ['jwt.verify']], function() {
    Route::get('/user', 'AuthController@getAuthenticatedUser');

    Route::get('/students','StudentController@index');
    Route::post('/student/{id}','StudentController@update');
    Route::delete('/student/{id}','StudentController@destroy');
    Route::get('/attendance','AttendanceController@index');
});

Route::group([
    'prefix' => 'auth'
], function ($router) {
    Route::post('/login', 'AuthController@login');
});
