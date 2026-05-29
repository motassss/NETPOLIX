const TOKEN_KEY = "netpolix_token";  // Clave para almacenar el token en localStorage

export const auth = { // export es tipo modulo reutilizable
    guardarToken(token)  {
        localStorage.setItem(TOKEN_KEY, token); 

    },
    obtenerToken() {
        return localStorage.getItem(TOKEN_KEY); 
    },
    eliminarToken() {
        localStorage.removeItem(TOKEN_KEY);
    },
    estaAutenticado() { // el usuario sigue loguiAo o que
        const token = this.obtenerToken();
        if (!token) return false;

        try {
            const payload = JSON.parse(atob(token.split(".")[1])); //header.payload.signature atob convierte base 64 a texto y JSON.PARSE convierte texto a objeto 
            const ahora = Date.now() / 1000;
        if (payload.exp <= ahora) {
                this.eliminarToken(); //LOGOUT AUTOMÁTICO
                return false;
            }

            return true;

        } catch {
            this.eliminarToken(); // token dañado
            return false;
        }
    }
};