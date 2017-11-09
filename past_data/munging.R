library(readr)
library(dplyr)

apps =  read_delim("~/Duke/DukeFall2017/CS 316/dukeConversations/past_data/raw_apps.txt", "\t", escape_double = FALSE, trim_ws = TRUE)
apps = as.data.frame(apps)
apps = select(apps, time, name, email, phone, year, major, reason, food, dinner, selected, skipped)
apps = filter(apps, year == 2017)
apps$phone = gsub("[a-zA-Z\\*\\(\\)\\_\\-]", "", apps$phone)
#munge email
apps$name = tolower(apps$name)
emails = unlist(strsplit(apps$email, "@"))
emails = emails[seq(1, length(emails), 2)]
apps$email = tolower(emails)


#create student df
names = unique(apps$name)
student = data.frame(uniqueID = NA, name = NA, phone = NA, netid = NA, year = NA, major = NA, pronouns = NA, food = NA)
i = 1
for (n in names) {
  temp = arrange(filter(apps, name == n), major)
  student[i,]$uniqueID = i
  student[i,c(2:6, 8)] = temp[1, c(2, 4, 3, 5, 6, 8)]
  i = i + 1
}
write.csv(student, file = "student.csv", row.names = FALSE)

#create application df
application = data.frame(dinnerID = NA, studentID = NA, datetime = NA, interest = NA, selected = NA, missed = NA)
for (i in 1:nrow(apps)){
  row = apps[i, ]
  n = as.character(row[2])
  sid = as.character(filter(student, name == n)[1])
  application[i, ] = c(row[9], sid, row[c(1, 7, 10, 11)])
  i = i + 1
}
write.csv(student, file = "application.csv", row.names = FALSE)