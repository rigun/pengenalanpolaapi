<?php

use Illuminate\Database\Seeder;

class UsersTableSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        $users = ['rio','agung','tedja','teguh','andrew'];
        foreach($users as $user){
            \App\User::create([
                'name' => $user,
                'email' => $user.'@email.com',
                'password' => bcrypt('password')
            ]);
        }
    }
}
