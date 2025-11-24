import { useState, useEffect } from 'react'

interface UserInfo {
  identityProvider: string
  userId: string
  userDetails: string
  userRoles: string[]
}

export function useAuth() {
  const [user, setUser] = useState<UserInfo | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/.auth/me')
      .then(res => res.json())
      .then(data => {
        if (data.clientPrincipal) {
          setUser(data.clientPrincipal)
        }
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [])

  const login = () => {
    window.location.href = '/.auth/login/aad'
  }

  const logout = () => {
    window.location.href = '/.auth/logout'
  }

  return { user, loading, login, logout }
}
