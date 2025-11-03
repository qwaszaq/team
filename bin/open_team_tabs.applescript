-- Opens Terminal with 8 tabs (Orchestrator + 7 agents) and sources their profiles
on run argv
  set base to "/Users/artur/coursor-agents-destiny-folder"
  set profilesDir to "/Users/artur/coursor-agents-destiny-folder/bin/profiles"
  tell application "Terminal"
    activate
    -- Orchestrator window/tab
    do script "cd " & quoted form of base & " ; source " & quoted form of (profilesDir & "/aleksander-nowak.sh") & " ; who ; /Users/artur/coursor-agents-destiny-folder/bin/bus_status.py"
    delay 0.2
    -- PM
    do script "cd " & quoted form of base & " ; source " & quoted form of (profilesDir & "/magdalena-kowalska.sh") & " ; who ; /Users/artur/coursor-agents-destiny-folder/bin/agent_copy_latest_prompt.py --agent 'Magdalena Kowalska' ; /Users/artur/coursor-agents-destiny-folder/bin/auto_handshake_ack.sh 'Magdalena Kowalska' 'Product Manager'" in window 1
    delay 0.2
    -- Architect
    do script "cd " & quoted form of base & " ; source " & quoted form of (profilesDir & "/katarzyna-wisniewska.sh") & " ; who ; /Users/artur/coursor-agents-destiny-folder/bin/agent_copy_latest_prompt.py --agent 'Katarzyna Wiśniewska' ; /Users/artur/coursor-agents-destiny-folder/bin/auto_handshake_ack.sh 'Katarzyna Wiśniewska' 'Architect'" in window 1
    delay 0.2
    -- Developer
    do script "cd " & quoted form of base & " ; source " & quoted form of (profilesDir & "/tomasz-zielinski.sh") & " ; who ; /Users/artur/coursor-agents-destiny-folder/bin/agent_copy_latest_prompt.py --agent 'Tomasz Zieliński' ; /Users/artur/coursor-agents-destiny-folder/bin/auto_handshake_ack.sh 'Tomasz Zieliński' 'Developer'" in window 1
    delay 0.2
    -- QA
    do script "cd " & quoted form of base & " ; source " & quoted form of (profilesDir & "/anna-nowakowska.sh") & " ; who ; /Users/artur/coursor-agents-destiny-folder/bin/agent_copy_latest_prompt.py --agent 'Anna Nowakowska' ; /Users/artur/coursor-agents-destiny-folder/bin/auto_handshake_ack.sh 'Anna Nowakowska' 'QA Engineer'" in window 1
    delay 0.2
    -- DevOps
    do script "cd " & quoted form of base & " ; source " & quoted form of (profilesDir & "/piotr-szymanski.sh") & " ; who ; /Users/artur/coursor-agents-destiny-folder/bin/agent_copy_latest_prompt.py --agent 'Piotr Szymański' ; /Users/artur/coursor-agents-destiny-folder/bin/auto_handshake_ack.sh 'Piotr Szymański' 'DevOps Engineer'" in window 1
    delay 0.2
    -- Security
    do script "cd " & quoted form of base & " ; source " & quoted form of (profilesDir & "/michal-dabrowski.sh") & " ; who ; /Users/artur/coursor-agents-destiny-folder/bin/agent_copy_latest_prompt.py --agent 'Michał Dąbrowski' ; /Users/artur/coursor-agents-destiny-folder/bin/auto_handshake_ack.sh 'Michał Dąbrowski' 'Security Specialist'" in window 1
    delay 0.2
    -- Data Scientist
    do script "cd " & quoted form of base & " ; source " & quoted form of (profilesDir & "/dr-joanna-wojcik.sh") & " ; who ; /Users/artur/coursor-agents-destiny-folder/bin/agent_copy_latest_prompt.py --agent 'Dr. Joanna Wójcik' ; /Users/artur/coursor-agents-destiny-folder/bin/auto_handshake_ack.sh 'Dr. Joanna Wójcik' 'Data Scientist'" in window 1
  end tell
end run
