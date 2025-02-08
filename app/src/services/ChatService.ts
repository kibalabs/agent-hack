export interface Message {
  content: string;
  isUser: boolean;
}

export interface ChatSession {
  messages: Message[];
  userId: string;
}

export interface ChatRequest {
  content: string;
  userId: string;
}

export interface ChatResponse {
  message: Message;
}

export class ChatService {
  private readonly baseUrl: string;

  public constructor(baseUrl: string = 'http://localhost:5000') {
    this.baseUrl = baseUrl;
  }

  public async sendMessage(content: string, userId: string): Promise<Message> {
    const request: ChatRequest = {
      content,
      userId,
    };
    const response = await fetch(`${this.baseUrl}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data: ChatResponse = await response.json();
    return data.message;
  }

  public async getChatHistory(userId: string): Promise<ChatSession> {
    const url = new URL(`${this.baseUrl}/chat/${userId}`);
    const response = await fetch(url.toString());
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data: ChatSession = await response.json();
    return data;
  }
}
