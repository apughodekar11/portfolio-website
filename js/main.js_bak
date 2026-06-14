// ============================================
// NAVIGATION
// ============================================

// Mobile menu toggle
const mobileMenuBtn = document.getElementById('mobile-menu-btn');
const mobileMenuClose = document.getElementById('mobile-menu-close');
const mobileMenu = document.getElementById('mobile-menu');

if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', () => {
        mobileMenu.classList.add('active');
        document.body.style.overflow = 'hidden';
    });
}

if (mobileMenuClose) {
    mobileMenuClose.addEventListener('click', () => {
        mobileMenu.classList.remove('active');
        document.body.style.overflow = '';
    });
}

// Close mobile menu on link click
document.querySelectorAll('.mobile-menu a').forEach(link => {
    link.addEventListener('click', () => {
        mobileMenu.classList.remove('active');
        document.body.style.overflow = '';
    });
});

// Navbar scroll effect
const navWrapper = document.getElementById('nav-wrapper');
window.addEventListener('scroll', () => {
    if (navWrapper) {
        if (window.scrollY > 50) {
            navWrapper.classList.add('scrolled');
        } else {
            navWrapper.classList.remove('scrolled');
        }
    }
});

// Active nav link on scroll
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav-links a');

function setActiveNavLink() {
    const scrollY = window.pageYOffset;

    sections.forEach(section => {
        const sectionHeight = section.offsetHeight;
        const sectionTop = section.offsetTop - 200;
        const sectionId = section.getAttribute('id');

        if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${sectionId}`) {
                    link.classList.add('active');
                }
            });
        }
    });
}

window.addEventListener('scroll', setActiveNavLink);

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// ============================================
// TYPEWRITER EFFECT
// ============================================

const typewriterElement = document.getElementById('typewriter');
const titles = ['DevOps Engineer', 'Cloud Engineer', 'SRE'];
let titleIndex = 0;
let charIndex = 0;
let isDeleting = false;
let typingSpeed = 100;

function typeWriter() {
    if (!typewriterElement) return;
    
    const currentTitle = titles[titleIndex];
    
    if (isDeleting) {
        typewriterElement.textContent = currentTitle.substring(0, charIndex - 1);
        charIndex--;
        typingSpeed = 50;
    } else {
        typewriterElement.textContent = currentTitle.substring(0, charIndex + 1);
        charIndex++;
        typingSpeed = 100;
    }

    if (!isDeleting && charIndex === currentTitle.length) {
        typingSpeed = 2000;
        isDeleting = true;
    } else if (isDeleting && charIndex === 0) {
        isDeleting = false;
        titleIndex = (titleIndex + 1) % titles.length;
        typingSpeed = 500;
    }

    setTimeout(typeWriter, typingSpeed);
}

// ============================================
// TERMINAL ANIMATION
// ============================================

const terminalContent = document.getElementById('terminal-content');

const terminalLines = [
    { type: 'prompt', text: 'apurva@cloud:~$ ', command: 'cat about.txt' },
    { type: 'blank' },
    { type: 'comment', text: '# Apurva Ghodekar' },
    { type: 'key-value', key: 'Role', value: 'DevOps Engineer & SRE' },
    { type: 'key-value', key: 'Location', value: 'Dublin, Ireland' },
    { type: 'key-value', key: 'Status', value: 'Available for opportunities' },
    { type: 'blank' },
    { type: 'heading', text: '# Core Expertise' },
    { type: 'list', text: 'Cloud Infrastructure (AWS)' },
    { type: 'list', text: 'Container Orchestration (Docker, Swarm)' },
    { type: 'list', text: 'Infrastructure as Code (Terraform)' },
    { type: 'list', text: 'Monitoring & Observability (Prometheus, Grafana)' },
    { type: 'list', text: 'Database Management (PostgreSQL, Cassandra)' },
    { type: 'blank' },
    { type: 'prompt', text: 'apurva@cloud:~$ ', command: './deploy.sh --env production' },
    { type: 'blank' },
    { type: 'success', text: 'Infrastructure validated' },
    { type: 'success', text: 'Docker services healthy' },
    { type: 'success', text: 'Monitoring active' },
    { type: 'cursor' }
];

function renderTerminal() {
    if (!terminalContent) return;
    
    let html = '';
    let lineIndex = 0;

    function addLine() {
        if (lineIndex >= terminalLines.length) return;

        const line = terminalLines[lineIndex];
        let lineHtml = '<div class="terminal-line">';

        switch (line.type) {
            case 'prompt':
                lineHtml += `<span class="terminal-prompt">${line.text}</span><span class="terminal-command">${line.command}</span>`;
                break;
            case 'blank':
                lineHtml += '&nbsp;';
                break;
            case 'comment':
                lineHtml += `<span class="terminal-comment">${line.text}</span>`;
                break;
            case 'key-value':
                lineHtml += `<span class="terminal-key">${line.key}:</span> <span class="terminal-value">${line.value}</span>`;
                break;
            case 'heading':
                lineHtml += `<span class="terminal-heading">${line.text}</span>`;
                break;
            case 'list':
                lineHtml += `<span class="terminal-list-item">${line.text}</span>`;
                break;
            case 'success':
                lineHtml += `<span class="terminal-success">${line.text}</span>`;
                break;
            case 'cursor':
                lineHtml += `<span class="terminal-prompt">apurva@cloud:~$ </span><span class="cursor-terminal"></span>`;
                break;
        }

        lineHtml += '</div>';
        html += lineHtml;
        terminalContent.innerHTML = html;

        lineIndex++;
        const delay = line.type === 'prompt' ? 300 : line.type === 'blank' ? 60 : 80;
        setTimeout(addLine, delay);
    }

    setTimeout(addLine, 800);
}

// ============================================
// SKILLS PROGRESS ANIMATION
// ============================================

function animateSkillProgress() {
    const progressCircles = document.querySelectorAll('.circular-progress');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const circle = entry.target;
                const progress = circle.dataset.progress;
                const progressCircle = circle.querySelector('.progress-circle');
                
                if (progressCircle) {
                    const circumference = 113; // 2 * PI * 18
                    const offset = circumference - (progress / 100) * circumference;
                    progressCircle.style.strokeDashoffset = offset;
                }
                
                observer.unobserve(circle);
            }
        });
    }, { threshold: 0.5 });

    progressCircles.forEach(circle => observer.observe(circle));
}

// ============================================
// EXPERIENCE TIMELINE ANIMATION
// ============================================

function animateTimeline() {
    const timelineItems = document.querySelectorAll('.timeline-item');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.classList.add('visible');
                }, index * 200);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.2 });

    timelineItems.forEach(item => observer.observe(item));
}

// ============================================
// PROJECTS FILTER & ANIMATION
// ============================================

function initProjectsFilter() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('.project-card');

    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            // Update active state
            filterButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const filter = btn.dataset.filter;

            projectCards.forEach(card => {
                if (filter === 'all' || card.dataset.type === filter) {
                    card.classList.remove('hidden');
                } else {
                    card.classList.add('hidden');
                }
            });
        });
    });

    // Fade in animation on scroll
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.classList.add('visible');
                }, index * 100);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    projectCards.forEach(card => observer.observe(card));
}

// ============================================
// CONTACT FORM
// ============================================

function initContactForm() {
    const form = document.getElementById('contact-form');
    
    if (!form) return;

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const submitBtn = form.querySelector('.form-submit');
        const originalContent = submitBtn.innerHTML;
        
        // Show loading state
        submitBtn.innerHTML = `
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="animation: spin 1s linear infinite;">
                <circle cx="12" cy="12" r="10" stroke-dasharray="32" stroke-dashoffset="32"></circle>
            </svg>
            Sending...
        `;
        submitBtn.disabled = true;
        
        // Simulate sending (replace with actual backend call later)
        setTimeout(() => {
            submitBtn.innerHTML = `
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
                Message Sent!
            `;
            submitBtn.style.background = 'var(--accent-green)';
            
            // Reset form
            form.reset();
            
            // Reset button after 3 seconds
            setTimeout(() => {
                submitBtn.innerHTML = originalContent;
                submitBtn.style.background = '';
                submitBtn.disabled = false;
            }, 3000);
        }, 1500);
    });
}

// ============================================
// INITIALIZE ON DOM LOAD
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    // Start typewriter
    setTimeout(typeWriter, 500);
    
    // Start terminal animation
    renderTerminal();
    
    // Initialize skills progress
    animateSkillProgress();
    
    // Initialize timeline
    animateTimeline();
    
    // Initialize projects filter
    initProjectsFilter();
    
    // Initialize contact form
    // initContactForm();

    // Auto-open Articles when coming from Blog link
    const params = new URLSearchParams(window.location.search);
    const filter = params.get('filter');

    if (filter === 'articles') {
        const articlesBtn = document.querySelector('[data-filter="article"]');
        if (articlesBtn) {
            articlesBtn.click();
        }
    }

});
