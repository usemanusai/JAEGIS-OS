# JAEGIS Cockpit

The JAEGIS Cockpit is a comprehensive web-based user interface that serves as the central command, control, and observability hub for the entire JAEGIS ecosystem.

## 🚀 Features

### EPIC 1: Foundation & Operations Dashboard
- **Real-time System Monitoring**: CPU, memory, disk usage with live updates
- **Active Agent Tracking**: Monitor A.C.I.D. agents and their status
- **Live Event Stream**: Real-time C.O.R.I. events with WebSocket updates
- **Service Health**: Monitor connectivity to all JAEGIS services

### EPIC 2: Forge Console & Taskmaster
- **Job Queue Management**: Track M.A.S.T.R. and A.S.C.E.N.D. forge operations
- **Task Status Monitoring**: Real-time progress tracking for all forge jobs
- **Detailed Job Views**: Comprehensive job details and error reporting
- **Filtering & Search**: Filter jobs by status, forge type, and date

### EPIC 3: Governance & Treasury
- **Approval Workflows**: Human-in-the-loop approval for new tools and agents
- **Budget Monitoring**: Real-time cost tracking and budget alerts
- **Spending Analytics**: Breakdown by category and service
- **Alert Management**: Configurable thresholds and notifications

## 🏗️ Architecture

### Backend (FastAPI)
- **Real-time API**: RESTful endpoints with WebSocket support
- **Service Integration**: Direct integration with JAEGIS core services
- **Database**: Uses existing S.C.R.I.P.T. SQLite backend
- **Event Logging**: Integrates with C.O.R.I. for pattern recognition

### Frontend (SvelteKit)
- **Responsive Design**: Mobile-first design with Tailwind CSS
- **Real-time Updates**: WebSocket connections for live data
- **Component Architecture**: Reusable UI components
- **State Management**: Reactive stores for data synchronization

### Core Services
- **SystemMonitor**: Real-time system metrics and health monitoring
- **TaskmasterService**: Job queue management for forge operations
- **GovernanceService**: Approval workflow management
- **TreasuryService**: Cost tracking and budget monitoring
- **WebSocketManager**: Real-time communication management

## 🚀 Quick Start

### Option 1: Automated Startup (Recommended)
```bash
cd jaegis_cockpit
python start_cockpit.py
```

This will:
1. Check all dependencies
2. Start the backend server
3. Provide instructions for starting the frontend

### Option 2: Manual Startup

#### Backend
```bash
cd jaegis_cockpit/backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8090
```

#### Frontend
```bash
cd jaegis_cockpit/frontend
npm install
npm run dev
```

### Access Points
- **Dashboard**: http://localhost:5173
- **API Documentation**: http://localhost:8090/docs
- **Backend Health**: http://localhost:8090/health

## 📡 API Endpoints

### System & Monitoring
- `GET /health` - Health check
- `GET /api/system/status` - System status information
- `WebSocket /ws/system-status` - Real-time system updates

### Taskmaster (Forge Operations)
- `GET /api/tasks` - List all tasks from Taskmaster
- `GET /api/tasks/{job_id}` - Get specific task details
- `GET /api/tasks/stats` - Get task statistics

### Governance (Approval Workflows)
- `GET /api/governance/approvals` - List approval requests
- `GET /api/governance/approvals/pending` - Get pending approvals
- `POST /api/governance/approvals/{id}/approve` - Approve request
- `POST /api/governance/approvals/{id}/reject` - Reject request

### Treasury (Cost Management)
- `GET /api/treasury/status` - Budget and cost information
- `GET /api/treasury/history` - Spending history

## 🔧 Integration with JAEGIS

The cockpit seamlessly integrates with existing JAEGIS frameworks:

### A.C.I.D. (Agent Orchestration)
- **Agent Monitoring**: Real-time agent count and status
- **Task Tracking**: Monitor swarm orchestration activities
- **Event Integration**: Receive orchestration events via C.O.R.I.

### C.O.R.I. (Cognitive Insights)
- **Event Stream**: Live display of C.O.R.I. events
- **Pattern Recognition**: Visual representation of detected patterns
- **Learning Triggers**: Monitor prediction errors and learning cycles

### M.A.S.T.R. (Tool Forge)
- **Job Tracking**: Monitor tool creation and validation jobs
- **Approval Integration**: Route new tools through governance workflow
- **Status Updates**: Real-time progress tracking

### A.S.C.E.N.D. (Agent Forge)
- **Agent Creation**: Monitor agent development jobs
- **Validation Results**: Display agent testing and validation
- **Deployment Tracking**: Track agent deployment status

### S.C.R.I.P.T. (Settings & Database)
- **Database Integration**: Uses existing SQLite backend
- **Settings Management**: Leverage existing configuration system
- **Data Persistence**: All cockpit data stored in S.C.R.I.P.T. database

## 🛠️ Development

### Project Structure
```
jaegis_cockpit/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main application
│   ├── services/           # Core services
│   └── requirements.txt    # Python dependencies
├── frontend/               # SvelteKit frontend
│   ├── src/
│   │   ├── routes/         # Page components
│   │   ├── lib/            # Shared components
│   │   └── app.css         # Global styles
│   └── package.json        # Node.js dependencies
└── start_cockpit.py        # Startup script
```

### Adding New Features

#### Backend Services
1. Create new service in `backend/services/`
2. Add service initialization in `main.py`
3. Create API endpoints for the service
4. Add database tables if needed

#### Frontend Pages
1. Create new route in `frontend/src/routes/`
2. Add navigation link in `+layout.svelte`
3. Create reusable components in `lib/components/`
4. Update API calls as needed

### Database Schema

The cockpit extends the S.C.R.I.P.T. database with new tables:

#### forge_jobs
- Stores M.A.S.T.R. and A.S.C.E.N.D. job information
- Tracks status, progress, and results
- Enables job queue management

#### approval_requests
- Manages governance approval workflows
- Stores validation results and decisions
- Tracks approval history

#### cost_entries
- Records spending and cost information
- Enables budget tracking and alerts
- Supports cost analytics

## 🔒 Security Considerations

- **CORS Configuration**: Properly configured for development
- **Input Validation**: All API inputs validated
- **Error Handling**: Graceful error handling and logging
- **Database Security**: Uses existing S.C.R.I.P.T. security model

## 🚦 Monitoring & Alerts

### System Health
- Real-time CPU, memory, and disk monitoring
- Service connectivity checks
- Automatic reconnection for WebSocket failures

### Budget Alerts
- Configurable spending thresholds
- Real-time budget utilization tracking
- Alert notifications for overspending

### Job Monitoring
- Failed job notifications
- Long-running job alerts
- Queue depth monitoring

## 📈 Performance

### Backend Optimization
- Async/await for non-blocking operations
- Connection pooling for database access
- Efficient WebSocket management
- Caching for frequently accessed data

### Frontend Optimization
- Component-based architecture for reusability
- Lazy loading for large datasets
- Efficient state management
- Optimized bundle sizes

## 🧪 Testing

### Backend Testing
```bash
cd backend
pytest tests/
```

### Frontend Testing
```bash
cd frontend
npm run test
```

## 📦 Deployment

### Production Deployment
1. Build frontend: `npm run build`
2. Configure production database
3. Set environment variables
4. Deploy with proper reverse proxy
5. Enable HTTPS and security headers

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d
```

## 🤝 Contributing

1. Follow existing code style and patterns
2. Add tests for new features
3. Update documentation
4. Test integration with JAEGIS services
5. Submit pull request with detailed description

## 📄 License

This project is part of the JAEGIS ecosystem and follows the same licensing terms.
