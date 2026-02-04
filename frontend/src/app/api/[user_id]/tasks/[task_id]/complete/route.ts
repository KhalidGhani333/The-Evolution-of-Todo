/**
 * Next.js API Route: Proxy for task completion toggle
 * Forwards requests to FastAPI backend with JWT authentication
 */
import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function PATCH(
  request: NextRequest,
  { params }: { params: Promise<{ user_id: string; task_id: string }> }
) {
  try {
    const { user_id, task_id } = await params;
    const token = request.headers.get('authorization');
    const body = await request.json();

    const response = await fetch(
      `${BACKEND_URL}/api/${user_id}/tasks/${task_id}/complete`,
      {
        method: 'PATCH',
        headers: {
          'Authorization': token || '',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      }
    );

    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error('Error toggling task completion:', error);
    return NextResponse.json(
      { error: 'Failed to toggle task completion' },
      { status: 500 }
    );
  }
}
