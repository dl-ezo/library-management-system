import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Button } from './ui/button';
import { Card, CardContent } from './ui/card';
import { User, LogOut } from 'lucide-react';

export function UserHeader() {
  const { user, logout } = useAuth();

  if (!user) return null;

  return (
    <Card className="mb-6">
      <CardContent className="p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-blue-100 p-2 rounded-full">
              <User className="w-5 h-5 text-blue-600" />
            </div>
            <div>
              <h2 className="font-semibold text-lg">{user.display_name}</h2>
              <p className="text-sm text-gray-600">@{user.username}</p>
            </div>
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={logout}
            className="flex items-center space-x-2"
          >
            <LogOut className="w-4 h-4" />
            <span>ログアウト</span>
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}