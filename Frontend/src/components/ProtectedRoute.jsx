import { Navigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import api from "../services/api";
import { REFRESH_TOKEN, ACCESS_TOKEN, IS_APPROVED } from "../constants";
import { useState, useEffect } from "react";
import PropTypes from "prop-types";

function ProtectedRoute({ children }) {
    const [isAuthorized, setIsAuthorized] = useState(null);

    useEffect(() => {
        auth().catch(() => setIsAuthorized(false))
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    const refreshToken = async () => {
        const refreshToken = localStorage.getItem(REFRESH_TOKEN);
        try {
            const res = await api.post("/api/auth/token/refresh/", {
                refresh: refreshToken,
            });
            if (res.status >= 200 && res.status < 300) {
                localStorage.setItem(ACCESS_TOKEN, res.data.access)
                setIsAuthorized(true)
            } else {
                setIsAuthorized(false)
            }
        } catch (error) {
            console.log(error);
            setIsAuthorized(false);
        }
    };

    const auth = async () => {
        const token = localStorage.getItem(ACCESS_TOKEN);
        if (!token) {
            setIsAuthorized(false);
            return;
        }
        const decoded = jwtDecode(token);
        const tokenExpiration = decoded.exp;
        const now = Date.now() / 1000;

        if (tokenExpiration < now) {
            await refreshToken();
        } else {
            setIsAuthorized(true);
        }
    };
    // Check if the user is approved
    

    if (isAuthorized === null) {
        return <div>Loading...</div>;
    }
    
    const isApproved = localStorage.getItem(IS_APPROVED);

    if (!isApproved) {
        return <Navigate to="/register" />;
    } else if (isApproved === "false") {
        return <Navigate to="/pending-approval" />;
    }

    return isAuthorized ? children : <Navigate to="/login" />;
}
ProtectedRoute.propTypes = {
    children: PropTypes.node.isRequired,
};
export default ProtectedRoute;