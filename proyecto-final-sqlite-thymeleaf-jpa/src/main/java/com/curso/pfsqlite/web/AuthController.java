package com.curso.pfsqlite.web;

import com.curso.pfsqlite.service.BusinessException;
import com.curso.pfsqlite.service.UsuarioService;
import com.curso.pfsqlite.web.form.RegisterForm;
import jakarta.validation.Valid;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

/*
 * ******************************************************************************************
 *  📚 PROYECTO FINAL - Spring Boot + Thymeleaf + SQLite + JPA
 *  🔹 CLASE: AuthController  |  CAPA: Web (Autenticación)
 *  🔐 USO EDUCATIVO EXCLUSIVO
 * ******************************************************************************************
 */

// * 🧠 TEORÍA: Este controlador gestiona las páginas de login y registro.
// ? El procesamiento del LOGIN lo hace Spring Security automáticamente (POST /login).
// ? Nosotros solo exponemos el GET /login para mostrar la página personalizada.
// ? El REGISTRO lo gestionamos nosotros: validamos el formulario y llamamos al service.

@Controller
public class AuthController {

    private final UsuarioService usuarioService;

    public AuthController(UsuarioService usuarioService) {
        this.usuarioService = usuarioService;
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 GET /login → página principal con modales de login y registro
    // ─────────────────────────────────────────────────────────────────────────

    // * 🧠 TEORÍA: Spring Security busca GET /login para mostrar el formulario.
    // ? Los parámetros ?error y ?logout los añade Spring Security automáticamente.
    // ? Siempre añadimos el form de registro vacío para que el modal funcione.
    @GetMapping("/login")
    public String loginPage(Model model) {
        if (!model.containsAttribute("registerForm")) {
            model.addAttribute("registerForm", new RegisterForm());
        }
        return "auth/login";
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 GET /register → redirige a la página de login con el modal abierto
    // ─────────────────────────────────────────────────────────────────────────

    @GetMapping("/register")
    public String registerPage() {
        return "redirect:/login?showRegister=true";
    }

    // ─────────────────────────────────────────────────────────────────────────
    // * 🔵 POST /register → procesa el registro de nuevo usuario
    // ─────────────────────────────────────────────────────────────────────────

    // * 🧠 TEORÍA: En caso de error NO hacemos redirect, sino que devolvemos la
    // ? vista auth/login directamente para preservar los errores de validación
    // ? en el modelo. La vista se encarga de abrir el modal de registro si hay errores.
    @PostMapping("/register")
    public String register(
            @Valid @ModelAttribute("registerForm") RegisterForm registerForm,
            BindingResult bindingResult,
            Model model,
            RedirectAttributes redirectAttributes) {

        if (bindingResult.hasErrors()) {
            model.addAttribute("showRegister", true);
            return "auth/login";
        }

        try {
            usuarioService.registrar(registerForm);
            redirectAttributes.addFlashAttribute("ok", "Usuario registrado. Ya puedes iniciar sesión.");
            return "redirect:/login";
        } catch (BusinessException ex) {
            bindingResult.rejectValue("username", "duplicate", ex.getMessage());
            model.addAttribute("showRegister", true);
            return "auth/login";
        }
    }
}
