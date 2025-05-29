// API client with authentication support
const API_URL = '/api';

class ApiClient {
  private getToken(): string | null {
    return localStorage.getItem('auth_token');
  }

  private getHeaders(): HeadersInit {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    const token = this.getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    return headers;
  }

  async request(endpoint: string, options: RequestInit = {}): Promise<Response> {
    const url = `${API_URL}${endpoint}`;
    const config: RequestInit = {
      ...options,
      headers: {
        ...this.getHeaders(),
        ...options.headers,
      },
    };

    const response = await fetch(url, config);
    
    // 認証エラーの場合はローカルストレージをクリア
    if (response.status === 401) {
      localStorage.removeItem('auth_token');
      localStorage.removeItem('auth_user');
      // 認証ページにリダイレクト（App.tsxのuseEffectで処理される）
      window.location.reload();
    }

    return response;
  }

  async get(endpoint: string): Promise<Response> {
    return this.request(endpoint, { method: 'GET' });
  }

  async post(endpoint: string, data?: unknown): Promise<Response> {
    return this.request(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async put(endpoint: string, data?: unknown): Promise<Response> {
    return this.request(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async delete(endpoint: string): Promise<Response> {
    return this.request(endpoint, { method: 'DELETE' });
  }
}

export const apiClient = new ApiClient();