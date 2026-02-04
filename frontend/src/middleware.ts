/**
 * Protected route middleware.
 * Redirects unauthenticated users to signin page.
 */
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const token = request.cookies.get("auth_token")?.value;

  // Protected routes that require authentication
  const protectedPaths = ["/tasks"];
  const isProtectedPath = protectedPaths.some((path) =>
    request.nextUrl.pathname.startsWith(path)
  );

  // Redirect to signin if accessing protected route without token
  if (isProtectedPath && !token) {
    return NextResponse.redirect(new URL("/signin", request.url));
  }

  // Redirect to tasks if accessing auth pages with valid token
  const authPaths = ["/signin", "/signup"];
  const isAuthPath = authPaths.some((path) =>
    request.nextUrl.pathname.startsWith(path)
  );

  if (isAuthPath && token) {
    return NextResponse.redirect(new URL("/tasks", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/tasks/:path*", "/signin", "/signup"],
};
