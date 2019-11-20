<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use JWTAuth;
use Tymon\JWTAuth\Exceptions\JWTException;

class AuthController extends Controller
{
    public function login(Request $request)
    {
      $credentials = $request->only(['email', 'password']);
      if (!$token = auth()->attempt($credentials)) {
        return response()->json(['error' => 'Unauthorized'], 401);
      }
      return $this->respondWithToken($token);
    }

    protected function respondWithToken($token)
    {
      return response()->json([
        'access_token' => $token,
        'token_type' => 'bearer'
      ]);
    }
    public function getAuthenticatedUser()
    {
      try {
        if (!$user = JWTAuth::parseToken()->authenticate()) {
          return response()->json(['msg'=>'user_not_found', 'stat' => '0'], 404);
        }
      } catch (Tymon\JWTAuth\Exceptions\TokenExpiredException $e) {
        return response()->json(['msg'=>'token_expired', 'stat' => '0'], $e->getStatusCode());
      } catch (Tymon\JWTAuth\Exceptions\TokenInvalidException $e) {
        return response()->json(['msg'=>'token_invalid', 'stat' => '0'], $e->getStatusCode());
      } catch (Tymon\JWTAuth\Exceptions\JWTException $e) {
        return response()->json(['msg'=>'token_absent', 'stat' => '0'], $e->getStatusCode());
      }
      return response()->json(['msg' => $user, 'stat' => '1']);
    }
}
