/**
 * Next.js API Route: Proxy for individual task operations
 * Forwards requests to FastAPI backend with JWT authentication
 */
import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ user_id: string; task_id: string }> }
) {
  try {
    const { user_id, task_id } = await params;
    const token = request.headers.get('authorization');

    const response = await fetch(
      `${BACKEND_URL}/api/${user_id}/tasks/${task_id}`,
      {
        method: 'GET',
        headers: {
          'Authorization': token || '',
          'Content-Type': 'application/json',
        },
      }
    );

    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error('Error fetching task:', error);
    return NextResponse.json(
      { error: 'Failed to fetch task' },
      { status: 500 }
    );
  }
}

export async function PUT(
  request: NextRequest,
  { params }: { params: Promise<{ user_id: string; task_id: string }> }
) {
  try {
    const { user_id, task_id } = await params;
    const token = request.headers.get('authorization');
    const body = await request.json();

    const response = await fetch(
      `${BACKEND_URL}/api/${user_id}/tasks/${task_id}`,
      {
        method: 'PUT',
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
    console.error('Error updating task:', error);
    return NextResponse.json(
      { error: 'Failed to update task' },
      { status: 500 }
    );
  }
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ user_id: string; task_id: string }> }
) {
  try {
    const { user_id, task_id } = await params;
    const token = request.headers.get('authorization');

    const response = await fetch(
      `${BACKEND_URL}/api/${user_id}/tasks/${task_id}`,
      {
        method: 'DELETE',
        headers: {
          'Authorization': token || '',
          'Content-Type': 'application/json',
        },
      }
    );

    if (response.status === 204) {
      return new NextResponse(null, { status: 204 });
    }

    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error('Error deleting task:', error);
    return NextResponse.json(
      { error: 'Failed to delete task' },
      { status: 500 }
    );
  }
}
