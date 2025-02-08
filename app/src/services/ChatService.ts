export interface Message {
  content: string;
  isUser: boolean;
}

export interface ChatHistory {
  messages: Message[];
}

export interface ChatRequest {
  content: string;
}

export interface ChatResponse {
  message: Message;
}

export interface AuthToken {
  message: string;
  signature: string;
}

export class ChatService {
  private readonly baseUrl: string;

  public constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  // eslint-disable-next-line class-methods-use-this, no-undef
  private getHeaders(authToken: AuthToken): HeadersInit {
    return {
      'Content-Type': 'application/json',
      Authorization: btoa(JSON.stringify(authToken)),
    };
  }

  public async sendMessage(content: string, userId: string, authToken: AuthToken): Promise<Message> {
    const request: ChatRequest = {
      content,
    };
    const response = await fetch(`${this.baseUrl}/chats/${userId}/messages`, {
      method: 'POST',
      headers: this.getHeaders(authToken),
      body: JSON.stringify(request),
      credentials: 'same-origin',
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data: ChatResponse = await response.json();
    return data.message;
  }

  public async getChatHistory(userId: string, authToken: AuthToken): Promise<ChatHistory> {
    const url = new URL(`${this.baseUrl}/chats/${userId}/history`);
    const response = await fetch(url.toString(), {
      method: 'GET',
      headers: this.getHeaders(authToken),
      credentials: 'same-origin',
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data: ChatHistory = await response.json();
    return data;
  }
}
